# Artwork

Sources of the app icon and logo. The house is inspired by the Home Assistant logo and uses the OpenObserve colours; the ring is inspired by the OpenObserve logo and uses Home Assistant blues.

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
