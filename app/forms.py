from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional
import re

def validate_username(form, field):
    if not re.match(r'^[a-zA-Z]+$', field.data):  # Только буквы
        raise ValidationError('Имя пользователя должно содержать только буквы.')

def validate_name(form, field):
    if not re.match(r'^[a-zA-Z]+$', field.data):
        raise ValidationError('Это поле должно содержать только буквы.')

def validate_phone(form, field):
    if not re.match(r'^[0-9]+$', field.data):
        raise ValidationError('Телефон должен содержать только цифры.')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message="Поле не может быть пустым"), validate_username])
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
    first_name = StringField('First Name', validators=[DataRequired(message="Поле не может быть пустым"), validate_name])
    second_name = StringField('Second Name', validators=[DataRequired(message="Поле не может быть пустым"), validate_name])
    phone = StringField('Phone', validators=[DataRequired(message="Поле не может быть пустым"), validate_phone])
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
