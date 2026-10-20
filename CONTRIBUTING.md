# Contributing to MECCHA CHAMELEON Trainer

Thanks for helping out with the MECCHA CHAMELEON Trainer! This is a community
project and PRs are welcome — but please read this first.

## Ground rules

- The trainer targets the **MECCHA CHAMELEON** game client (Steam build, 2026).
- Do not submit offsets for region-locked builds without a version tag.
- Keep the plugin API stable. Breaking changes to `core/contracts.py` need a
  version bump in `core/registry.py` and a migration note in `CHANGELOG.md`.
- No obfuscated code. Everything must be readable Python.

## Dev setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m meccha_trainer --dry-run
```

## Adding a plugin

1. Drop a package under `plugins/` (see `plugins/aim_assist/` for a template).
2. Declare `PLUGIN_MANIFEST` in `__init__.py` — see `core/contracts.py`.
3. Register any hotkeys in `config/default.yaml` under `hotkeys:`.
4. Add a smoke test in `tests/`.

## Style

- Python 3.11+, type hints everywhere.
- `ruff` + `black` defaults.
- No `print()` in plugin code — use `utils.logging.get_logger(__name__)`.

## Reporting bugs

Open an issue with the trainer version, game build hash (from
`Help → About → Build Hash`), and a log tail from `logs/trainer.log`.

Use at your own risk. This is a hobbyist project for educational modding research.