import smtplib
from email.message import EmailMessage
from flask import current_app

def send_reset_email(to_email: str, reset_url: str) -> None:
    """Send password reset email.

    If MAIL_SERVER is not configured, this function prints the URL to console.
    """
    server = current_app.config.get("MAIL_SERVER", "")
    if not server:
        print("\n=== Password reset demo ===")
        print(f"To: {to_email}")
        print(f"Reset URL: {reset_url}")
        print("=== End demo ===\n")
        return

    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = current_app.config.get("MAIL_DEFAULT_SENDER")
    msg["To"] = to_email
    msg.set_content(
        "You requested a password reset. Use this link (valid for 1 hour):\n\n"
        f"{reset_url}\n\n"
        "If you didn't request this, ignore this email."
    )

    port = current_app.config.get("MAIL_PORT", 587)
    use_tls = current_app.config.get("MAIL_USE_TLS", True)
    username = current_app.config.get("MAIL_USERNAME", "")
    password = current_app.config.get("MAIL_PASSWORD", "")

    if use_tls:
        with smtplib.SMTP(server, port) as smtp:
            smtp.starttls()
            if username and password:
                smtp.login(username, password)
            smtp.send_message(msg)
    else:
        with smtplib.SMTP(server, port) as smtp:
            if username and password:
                smtp.login(username, password)
            smtp.send_message(msg)
