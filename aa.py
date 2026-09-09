from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class Registration(FlaskForm):

    name = StringField(
        "Full name",
        validators=[DataRequired()],
        render_kw={"class": "auth-input", "placeholder": "e.g. Umar Khan"}
    )

    email = StringField(
        "Email address",
        validators=[DataRequired(), Email()],
        render_kw={"class": "auth-input", "placeholder": "you@example.com"}
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=6)],
        render_kw={"class": "auth-input", "placeholder": "At least 6 characters"}
    )

    submit = SubmitField("Create Account", render_kw={"class": "scan-btn"})