# Quilt Bee

Quilt block designer and quilt planner. Single-file web app, no build step.

- `index.html` — the editor. Open it in a browser, or publish as an artifact.
  Live prototype: https://claude.ai/artifact/5pTVtrjS2gbTQBPRsYTk4Z
- `research/validation-report.html` — go/no-go validation (demand, competitors, review mining, tail check, wireframes, pricing).
  Published: https://claude.ai/artifact/MidypbcJCV5d13ZfADW2Vs
- `research/` — raw data behind the report: App Store reviews (`quilt_reviews*.json`), every quilt app found (`quilt_apps.json`),
  Google autocomplete demand harvest (`demand.txt`, `harvest.sh`), App Store supply scripts (`supply.py`, `supply2.py`).

Validation gate (from the report): put the editor in front of five quilters. If three build a block without asking a
question, build the app. If they reach for graph paper, stop.
