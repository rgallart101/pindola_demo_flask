from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_babel import lazy_gettext as _l

class RegisterForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField(_l("Email"), validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=8, max=128)])
    password2 = PasswordField(_l("Confirm password"), validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(_l("Create account"))

class LoginForm(FlaskForm):
    username = StringField(_l("Username"), validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField(_l("Password"), validators=[DataRequired(), Length(min=1, max=128)])
    remember = BooleanField(_l("Remember me"))
    submit = SubmitField(_l("Log in"))

class MFATokenForm(FlaskForm):
    token = StringField(_l("6-digit code"), validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField(_l("Verify"))

class ForgotPasswordForm(FlaskForm):
    email = StringField(_l("Email"), validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField(_l("Send reset link"))

class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l("New password"), validators=[DataRequired(), Length(min=8, max=128)])
    password2 = PasswordField(_l("Confirm new password"), validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField(_l("Reset password"))

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(_l("Current password"), validators=[DataRequired()])
    new_password = PasswordField(_l("New password"), validators=[DataRequired(), Length(min=8, max=128)])
    new_password2 = PasswordField(_l("Confirm new password"), validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField(_l("Update password"))
