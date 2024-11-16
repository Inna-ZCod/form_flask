from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

# Форма регистрации пользователя
class RegistrationForm(FlaskForm):
    # Поле для ввода имени пользователя с проверкой обязательности и длины
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # Поле для ввода email с проверкой обязательности и формата email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Поле для ввода пароля с проверкой обязательности и минимальной длины
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    # Поле для подтверждения пароля с проверкой на совпадение с полем пароля
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    # Кнопка для отправки формы регистрации
    submit = SubmitField('Register')

# Форма для авторизации пользователя
class LoginForm(FlaskForm):
    # Поле для ввода email с проверкой обязательности и формата email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Поле для ввода пароля с проверкой обязательности
    password = PasswordField('Password', validators=[DataRequired()])
    # Кнопка для отправки формы авторизации
    submit = SubmitField('Login')

# Форма для обновления профиля пользователя
class UpdateProfileForm(FlaskForm):
    # Поле для ввода нового имени пользователя с проверкой обязательности и длины
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    # Поле для ввода нового email с проверкой обязательности и формата email
    email = StringField('Email', validators=[DataRequired(), Email()])
    # Поле для ввода нового пароля с проверкой минимальной длины (необязательно)
    password = PasswordField('New Password', validators=[Length(min=6)])
    # Кнопка для отправки формы обновления профиля
    submit = SubmitField('Update')
