from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SubmitField, validators
from wtforms.validators import ValidationError, DataRequired, EqualTo, Length

#Defines fields in registration and login forms. Includes definitions of validators.

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    register = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Enter your password', validators=[DataRequired()])
    login = SubmitField('Login')
