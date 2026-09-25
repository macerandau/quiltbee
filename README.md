# Quilt Bee

Quilt block designer and quilt planner. The app is a single HTML file with no build step.

- `docs/index.html` — the app. Served publicly by GitHub Pages at https://quiltbee.app/ (GitHub Pages, custom domain) and bundled into the iOS shell.
- `docs/privacy.html`, `docs/support.html` — the pages the App Store listing links to.
- `icon.svg` — the mark. Rasterize with `magick -background none -density 384 icon.svg -resize 512x512 docs/icon-512.png`.
- `art/` — the bee artwork sources.
- `ios/` — Capacitor iOS shell (`npx cap sync ios` copies `docs/` into it). Purchases use cordova-plugin-purchase; product `com.quiltbee.app.plus`.
- `codemagic.yaml` — builds and signs on Codemagic and uploads to TestFlight on every push to master.
- `research/` — the niche validation report and the scripts behind it.

Free: baby and lap quilts, and the first throw. Quilt Bee Plus ($19.99 once): bed sizes and unlimited throws.
