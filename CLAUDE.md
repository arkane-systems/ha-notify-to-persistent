# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

`notify_to_persistent` is a Home Assistant custom component (distributed via HACS) that bridges HA's `notify` entity platform to `persistent_notification.create`. It exposes exactly one notify entity, created by a single, zero-config config entry; any message (with optional title) sent to that entity becomes a new persistent notification. Minimum supported Home Assistant version: 2024.5.0, the release that introduced `NotifyEntity` (see `hacs.json`).

There is no build system or linter configured in this repo. CI runs three GitHub Actions on every push/PR: `hassfest` (`.github/workflows/hassfest.yml`), which validates the integration's manifest/structure against Home Assistant's core requirements; `hacs` (`.github/workflows/hacs.yml`), which validates HACS-repository requirements; and `test` (`.github/workflows/test.yml`), which runs the pytest suite.

## Testing

Tests use [`pytest-homeassistant-custom-component`](https://pypi.org/project/pytest-homeassistant-custom-component/), which provides a real (in-memory) `hass` fixture and HA test helpers without needing a full Home Assistant core checkout. Set up and run:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements_test.txt
pytest tests/                      # full suite
pytest tests/test_config_flow.py   # single file
pytest tests/test_notify.py::test_send_message_creates_persistent_notification_with_title  # single test
```

`requirements_test.txt` pins `pytest-homeassistant-custom-component`, which in turn pins a compatible `homeassistant` core version — bump it deliberately, not incidentally, since it determines which HA APIs the tests exercise. `pytest.ini` sets `asyncio_mode = auto` (required for the `async def test_...` tests here).

**Custom component discovery gotcha:** `pytest-homeassistant-custom-component` ships its own `custom_components` package (with an `__init__.py`) inside its installed `testing_config` dir. Because Python's import system resolves a *regular* package (one with `__init__.py`) before merging any namespace packages, a bare `hass.config_entries.async_setup(...)` in a test would silently fail to find `notify_to_persistent` unless something extends `custom_components.__path__` to include this repo's `custom_components/` dir. `tests/conftest.py` does this once at collection time, and also wires up the `enable_custom_integrations` fixture as `autouse` so every test can load the integration without asking for it explicitly. If integration discovery starts failing in a new HA version, this is the first place to check — the `_get_custom_components()` implementation in `homeassistant/loader.py` is the reference for how it actually resolves integrations.

## Architecture

```
ConfigFlow (config_flow.py)
    → zero fields; async_set_unique_id(DOMAIN) + _abort_if_unique_id_configured()
      enforces single-instance
    → async_create_entry(data={}) — nothing to store
        → async_setup_entry (__init__.py)
            → forwards to notify platform → PersistentNotifyEntity (notify.py)
                → notify.send_message (message + optional title)
                    → hass.services.async_call("persistent_notification", "create", ...)
```

### Key files

| File | Purpose |
|---|---|
| `custom_components/notify_to_persistent/config_flow.py` | Zero-input, single-instance config flow. |
| `custom_components/notify_to_persistent/notify.py` | `PersistentNotifyEntity` — the whole functional core. |
| `custom_components/notify_to_persistent/__init__.py` | Forwards the config entry to the `notify` platform. |
| `custom_components/notify_to_persistent/manifest.json` | No `single_config_entry` key — single-instance is enforced in `config_flow.py` via unique_id, not the manifest key (kept consistent with this author's other integrations). |

No `notification_id` is ever passed to `persistent_notification.create`, so every `send_message` call produces a distinct, accumulating notification rather than overwriting a previous one — this is a deliberate design choice, not an oversight.

### Things to keep in sync

`strings.json` and `custom_components/notify_to_persistent/translations/en.json` must stay identical — the former is the source HA reads at development time, the latter is what ships and is what Lokalise-style translation tooling would pick up.
