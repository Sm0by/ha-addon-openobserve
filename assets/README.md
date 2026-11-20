# Artwork

Sources of the app icon and logo: a plain house in the OpenObserve colours with a pulse line, inside a ring of four arcs in Home Assistant blues.

Keep the artwork clearly distinct from the trademarked logos of Home Assistant and OpenObserve: no antenna or nodes of the Home Assistant logo, no copied paths or exact colour sets of either logo.

| File | Use |
|---|---|
| `icon.svg` | Source of `openobserve/icon.png` (square) |
| `logo.svg` | Source of `openobserve/logo.png` (250×100) |
| `gen-logo.js` | Generates both SVGs: `node gen-logo.js assets` |
| `render.sh` | Renders an SVG to PNG with headless Microsoft Edge on Windows (Git Bash) |

The PNGs are rendered at twice the recommended size for sharp display on high-resolution screens:

```bash
bash assets/render.sh assets/icon.svg openobserve/icon.png 128 128 2
bash assets/render.sh assets/logo.svg openobserve/logo.png 250 100 2
```
