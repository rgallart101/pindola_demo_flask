# Píndola Vermella – Password Manager Demo (Flask)

A small demo webapp (Pinterest-ish grid) to showcase:
- Register / Login / Forgot password
- Password change
- MFA (TOTP / Google Authenticator)
- **Multilingual Support (English & Catalan)** 🌐
- Dashboard + logout

## Quick start

```bash
# 1) Create venv
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
# .venv\Scripts\activate  # Windows PowerShell

# 2) Install deps
pip install -r requirements.txt

# 3) Run
python run.py
```

Then open: http://127.0.0.1:5000

The SQLite database will be created automatically in `instance/app.db`.

## Makefile

The project includes a `Makefile` with convenient targets. By default the Makefile will use the project's virtual environment Python at `.venv/bin/python` if it exists, otherwise it falls back to the system `python`.

Common targets:

- Compile translations:

```bash
make compile-language
```

- Remove compiled Python artefacts (`__pycache__`, `.pyc`):

```bash
make clean
```

- Serve the application (runs `python run.py`):

```bash
make serve
```

You can override the Python binary used by the Makefile with the `PYTHON` environment variable, for example:

```bash
PYTHON=python3.11 make compile-language
```

- Detect new/untranslated strings (extracts POT and reports untranslated msgids):

```bash
make detect-new
```

This target runs `pybabel extract` to refresh `app/translations/messages.pot` and then scans each locale's `messages.po` to report untranslated entries and examples.


## Email (Forgot Password)

This project includes a **placeholder** mail configuration. If you don't configure mail,
the app will print the reset URL to the terminal so you can demo the flow locally.

To configure real SMTP, copy `.env.example` to `.env` and edit values.

> Tip: For tutorials, you can keep SMTP disabled and just use the console link.

## Multilingual Support 🌐

The application supports **English** and **Catalan**. Users can switch languages using the globe icon (🌐) in the navigation bar.

- All UI strings are translatable
- Language preference is stored in the user session
- Browser language is used as fallback
- Full Catalan translation included

For more details on adding translations or supporting new languages, see [MULTILINGUAL.md](MULTILINGUAL.md).

## Development: FLASK_DEBUG

- **Variable**: FLASK_DEBUG — Enables Flask's debug mode; set in [.env](.env).
- **How to set**: add `FLASK_DEBUG=1` (or `true`) in `.env`; the app reads it via [app/config.py](app/config.py) and `run.py` uses it to set Flask's `debug` flag.
- **Run**: start the app with `python run.py` or `make serve` to pick up the flag from `.env`.
- **Warning**: Only enable `FLASK_DEBUG` in development. Do NOT set it to `1`/`true` in production — the interactive debugger can execute code and expose sensitive data.

## Notes

- Passwords are hashed with Werkzeug.
- MFA uses TOTP (RFC 6238) via `pyotp`.
- CSRF protection is enabled via Flask-WTF.
- Translations managed with Flask-Babel.

