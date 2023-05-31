from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import EqualTo, InputRequired


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password')])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField()


class PostForm(FlaskForm):
    brand = StringField('Brand', validators=[InputRequired()])
    alcohol_level = StringField('Alcohol level', validators=[InputRequired()])
    class_alcohol = StringField('Class alcohol', validators=[InputRequired()])
    submit = SubmitField()