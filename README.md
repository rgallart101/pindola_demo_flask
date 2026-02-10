# Píndola Vermella – Password Manager Demo (Flask)

A small demo webapp (Pinterest-ish grid) to showcase:
- Register / Login / Forgot password
- Password change
- MFA (TOTP / Google Authenticator)
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

## Email (Forgot Password)

This project includes a **placeholder** mail configuration. If you don't configure mail,
the app will print the reset URL to the terminal so you can demo the flow locally.

To configure real SMTP, copy `.env.example` to `.env` and edit values.

> Tip: For tutorials, you can keep SMTP disabled and just use the console link.

## Notes

- Passwords are hashed with Werkzeug.
- MFA uses TOTP (RFC 6238) via `pyotp`.
- CSRF protection is enabled via Flask-WTF.
