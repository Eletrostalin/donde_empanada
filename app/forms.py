from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
import re

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Поле не может быть пустым")])
    email = StringField('Email', validators=[Optional(), Email(message="Неправильный формат email")])
    password = PasswordField('Password', validators=[
        DataRequired(message="Поле не может быть пустым"),
        Length(min=8, message="Пароль должен содержать минимум 8 символов"),
        lambda form, field: re.match(r'^(?=.*[a-z])(?=.*\d).+$', field.data) or ValidationError(
            "Пароль должен содержать цифры и строчные буквы"
        )
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(message="Поле не может быть пустым"),
        EqualTo('password', message="Пароли должны совпадать")
    ])
    first_name = StringField('First Name', validators=[DataRequired(message="Поле не может быть пустым")])
    second_name = StringField('Second Name', validators=[DataRequired(message="Поле не может быть пустым")])
    phone = StringField('Phone', validators=[DataRequired(message="Поле не может быть пустым")])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class LocationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    working_hours = StringField('Working Hours', validators=[DataRequired()])
    average_check = IntegerField('Average Check', validators=[DataRequired()])  # Изменение типа на Integer
    submit = SubmitField('Add Location')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Add Review')
