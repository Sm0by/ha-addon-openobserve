"""Validate the app against the Home Assistant Supervisor's own schemas.

Run with a Supervisor checkout on PYTHONPATH. Collects schema errors and the
deprecation warnings the Supervisor logs while reading the app, writes them as
Markdown and exits with 1 if anything was found.
"""

import argparse
import importlib
import logging
from pathlib import Path
import sys

import voluptuous as vol
from voluptuous.humanize import humanize_error
import yaml


class Collector(logging.Handler):
    """Keep every warning the Supervisor logs."""

    def __init__(self) -> None:
        super().__init__(logging.WARNING)
        self.messages: list[str] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.messages.append(record.getMessage())


def first_attr(module_names: list[str], attr_names: list[str]):
    """Return the first attribute found (the Supervisor renamed addons to apps)."""
    for module_name in module_names:
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            continue
        for attr_name in attr_names:
            if hasattr(module, attr_name):
                return getattr(module, attr_name)
    raise SystemExit(f"None of {attr_names} found in {module_names}")


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


def validate(schema, path: Path, root: Path, findings: list[str], collector: Collector):
    """Validate one file and record errors and warnings."""
    collector.messages.clear()
    rel = path.relative_to(root)
    try:
        data = load_yaml(path)
        schema(data)
    except vol.Invalid as err:
        findings.append(f"- **Error** `{rel}`: {humanize_error(data, err)}")
    except yaml.YAMLError as err:
        findings.append(f"- **Error** `{rel}`: cannot be parsed ({err})")
    for message in collector.messages:
        findings.append(f"- **Warning** `{rel}`: {message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repository root")
    parser.add_argument("--app", required=True, help="App folder, e.g. openobserve")
    parser.add_argument("--report", required=True, help="Markdown report to write")
    parser.add_argument("--label", required=True, help="Heading for the report")
    args = parser.parse_args()

    collector = Collector()
    supervisor_logger = logging.getLogger("supervisor")
    supervisor_logger.setLevel(logging.WARNING)
    supervisor_logger.addHandler(collector)
    supervisor_logger.propagate = False

    validate_modules = ["supervisor.apps.validate", "supervisor.addons.validate"]
    schema_config = first_attr(validate_modules, ["SCHEMA_APP_CONFIG", "SCHEMA_ADDON_CONFIG"])
    schema_translations = first_attr(
        validate_modules, ["SCHEMA_APP_TRANSLATIONS", "SCHEMA_ADDON_TRANSLATIONS"]
    )
    schema_build = first_attr(validate_modules, ["SCHEMA_BUILD_CONFIG"])
    schema_repository = first_attr(["supervisor.store.validate"], ["SCHEMA_REPOSITORY_CONFIG"])

    root = Path(args.root).resolve()
    app = root / args.app
    findings: list[str] = []

    configs = [p for p in (app / f"config.{ext}" for ext in ("yaml", "yml", "json")) if p.exists()]
    if not configs:
        findings.append(f"- **Error** no config.yaml found in `{args.app}`")
    for path in configs:
        validate(schema_config, path, root, findings, collector)

    for path in sorted((app / "translations").glob("*")):
        if path.suffix in (".yaml", ".yml", ".json"):
            validate(schema_translations, path, root, findings, collector)

    for path in (app / f"build.{ext}" for ext in ("yaml", "yml", "json")):
        if path.exists():
            findings.append(
                f"- **Warning** `{path.relative_to(root)}`: build files are deprecated, "
                "move the build parameters into the Dockerfile"
            )
            validate(schema_build, path, root, findings, collector)

    for path in (root / f"repository.{ext}" for ext in ("yaml", "yml", "json")):
        if path.exists():
            validate(schema_repository, path, root, findings, collector)

    lines = [f"### {args.label}", ""]
    lines += findings or ["No errors or deprecation warnings."]
    Path(args.report).write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
