from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError
from models import Profile
import re


class RegisterProfile(FlaskForm):
    username = StringField(label="Enter username: ", validators=[DataRequired()])
    email = EmailField(label="Enter email: ", validators=[DataRequired()])
    password1 = PasswordField(label="Enter password: ", validators=[DataRequired()])
    password2 = PasswordField(label="Submit password: ", validators=[DataRequired(), EqualTo("password1")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        profile = Profile.query.filter_by(username=username.data).first()
        if profile:
            raise ValidationError("This account already exists ")

    def validate_email(self, email):
        profile = Profile.query.filter_by(email=email.data).first()
        if profile:
            raise ValidationError("This account already exists")

    def validate_password1(self, password):
        self.password = password.data
        self.checker = re.compile("^(?=\S{8,20}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])")
        if not self.checker.search(self.password):
            raise ValidationError("This password is incorrect")


class Login(FlaskForm):
    email = EmailField(label="Enter email: ", validators=[DataRequired()])
    password = PasswordField(label="Enter password: ", validators=[DataRequired()])
    submit = SubmitField("Login")


class RegisterPost(FlaskForm):
    name = StringField(label="Enter name: ", validators=[DataRequired()])
    body = TextAreaField(label="Enter body: ", validators=[DataRequired()])
    submit = SubmitField("Post")


