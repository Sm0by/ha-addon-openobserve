#!/usr/bin/env bash
# render.sh <svg> <png> <width> <height> [scale]
# Renders an SVG to a PNG with a transparent background using headless Edge.
set -euo pipefail
svg="$(cygpath -w "$(realpath "$1")")"
png="$(cygpath -w "$(realpath -m "$2")")"
scale="${5:-1}"
"/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
  --headless=new --disable-gpu --hide-scrollbars \
  --default-background-color=00000000 \
  --force-device-scale-factor="$scale" \
  --window-size="$3,$4" \
  --screenshot="$png" "file:///${svg//\\//}" 2>/dev/null
ls -la "$2"
