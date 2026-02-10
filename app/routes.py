from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_

from . import db
from .models import User
from .forms import (
    RegisterForm, LoginForm, MFATokenForm, ForgotPasswordForm,
    ResetPasswordForm, ChangePasswordForm
)
from .tokens import make_reset_token, verify_reset_token
from .email_utils import send_reset_email
from .mfa_utils import generate_secret, provisioning_uri, verify_token, qr_code_data_uri

auth_bp = Blueprint("auth", __name__)

@auth_bp.get("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))
    return redirect(url_for("auth.login"))

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter(
            or_(User.username == form.username.data, User.email == form.email.data)
        ).first()
        if existing:
            flash("Username or email already exists.", "danger")
            return render_template("register.html", form=form)

        user = User(username=form.username.data.strip(), email=form.email.data.strip().lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        flash("Account created. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data.strip()).first()
        if not user or not user.check_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return render_template("login.html", form=form)

        # MFA flow
        if user.mfa_enabled and user.mfa_secret:
            session["pre_2fa_user_id"] = user.id
            session["remember_me"] = bool(form.remember.data)
            return redirect(url_for("auth.mfa_verify"))

        login_user(user, remember=form.remember.data)
        return redirect(url_for("auth.dashboard"))

    return render_template("login.html", form=form)

@auth_bp.route("/mfa", methods=["GET", "POST"])
def mfa_verify():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    uid = session.get("pre_2fa_user_id")
    if not uid:
        return redirect(url_for("auth.login"))

    user = db.session.get(User, int(uid))
    if not user or not user.mfa_enabled or not user.mfa_secret:
        session.pop("pre_2fa_user_id", None)
        return redirect(url_for("auth.login"))

    form = MFATokenForm()
    if form.validate_on_submit():
        token = form.token.data.strip()
        if verify_token(user.mfa_secret, token):
            remember = session.get("remember_me", False)
            login_user(user, remember=remember)
            session.pop("pre_2fa_user_id", None)
            session.pop("remember_me", None)
            return redirect(url_for("auth.dashboard"))
        flash("Invalid code. Try again.", "danger")

    return render_template("mfa_verify.html", form=form, username=user.username)

@auth_bp.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    form = ForgotPasswordForm()
    if form.validate_on_submit():
        # Avoid user enumeration: show same message even if email doesn't exist.
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user:
            token = make_reset_token(user.id)
            reset_url = current_app.config["APP_URL"].rstrip("/") + url_for("auth.reset_password", token=token)
            send_reset_email(to_email=user.email, reset_url=reset_url)

        flash("If that email exists, a reset link has been sent.", "info")
        return redirect(url_for("auth.login"))

    return render_template("forgot_password.html", form=form)

@auth_bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for("auth.dashboard"))

    user_id = verify_reset_token(token)
    if not user_id:
        flash("This reset link is invalid or expired.", "danger")
        return redirect(url_for("auth.forgot_password"))

    user = db.session.get(User, int(user_id))
    if not user:
        flash("This reset link is invalid.", "danger")
        return redirect(url_for("auth.forgot_password"))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Password updated. You can log in now.", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", form=form)

@auth_bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash("Current password is incorrect.", "danger")
            return render_template("change_password.html", form=form)

        current_user.set_password(form.new_password.data)
        db.session.commit()
        flash("Password updated.", "success")
        return redirect(url_for("auth.dashboard"))

    return render_template("change_password.html", form=form)

@auth_bp.route("/enable-mfa", methods=["GET", "POST"])
@login_required
def enable_mfa():
    # If already enabled, allow re-viewing / re-seeding for demo simplicity
    if not current_user.mfa_secret:
        current_user.mfa_secret = generate_secret()
        db.session.commit()

    uri = provisioning_uri(current_user.mfa_secret, current_user.username, issuer_name="Pindola Vermella Demo")
    qr = qr_code_data_uri(uri)

    form = MFATokenForm()
    if form.validate_on_submit():
        token = form.token.data.strip()
        if verify_token(current_user.mfa_secret, token):
            current_user.mfa_enabled = True
            db.session.commit()
            flash("MFA enabled!", "success")
            return redirect(url_for("auth.dashboard"))
        flash("Invalid code. Make sure you scanned the QR and try again.", "danger")

    return render_template("enable_mfa.html", form=form, qr_data_uri=qr, uri=uri, mfa_enabled=current_user.mfa_enabled)

@auth_bp.get("/dashboard")
@login_required
def dashboard():
    # mock image filenames
    images = [f"images/{i}.svg" for i in range(1, 10)]
    return render_template("dashboard.html", images=images)

@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out.", "info")
    return redirect(url_for("auth.login"))
