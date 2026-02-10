from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    password2 = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create account")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=1, max=128)])
    remember = BooleanField("Remember me")
    submit = SubmitField("Log in")

class MFATokenForm(FlaskForm):
    token = StringField("6-digit code", validators=[DataRequired(), Length(min=6, max=6)])
    submit = SubmitField("Verify")

class ForgotPasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    submit = SubmitField("Send reset link")

class ResetPasswordForm(FlaskForm):
    password = PasswordField("New password", validators=[DataRequired(), Length(min=8, max=128)])
    password2 = PasswordField("Confirm new password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Reset password")

class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Current password", validators=[DataRequired()])
    new_password = PasswordField("New password", validators=[DataRequired(), Length(min=8, max=128)])
    new_password2 = PasswordField("Confirm new password", validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Update password")
