import string

from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

from models import User

data_required = DataRequired('Заполните это поле')
email = Email('Некорректный email')


class LoginForm(FlaskForm):
    login = StringField('Логин', validators=[data_required])
    password = PasswordField('Пароль', validators=[data_required])
    submit = SubmitField('Войти')


class RegisterForm(FlaskForm):
    email = EmailField('Почта', validators=[email])
    login = StringField('Логин', validators=[data_required, Length(min=6, message='Логин должен быть не '
                                                                                  'менее 6 символов')])
    password1 = PasswordField('Пароль', validators=[data_required, Length(min=8,
                                                                          message='Пароль должен быть не '
                                                                                  'менее 8 символов')])
    password2 = PasswordField('Пароль ещё раз', validators=[data_required, EqualTo('password1',
                                                                                   message='Пароли должны совпадать')])
    submit = SubmitField('Зарегистрироваться')

    # Validate login
    @staticmethod
    def validate_login(_, login):
        if login.data[0].lower() not in string.ascii_lowercase:
            raise ValidationError("Логин должен начинаться с буквы")
        if len(set(login.data).intersection(set(string.ascii_letters + string.digits + '_'))) != len(set(login.data)):
            raise ValidationError("Логин должен содержать только символы латинского алфавита, цифры и знак \"_\"")

        return True

    # Validate password
    @staticmethod
    def validate_password1(_, password):
        if not (len(set(password.data).intersection(set(string.ascii_uppercase))) >= 1 and len(
                set(password.data).intersection(set(string.ascii_lowercase))) >= 1 and len(
            set(password.data).intersection(set(string.digits))) >= 1 and len(
            set(password.data).intersection(set(string.punctuation + "%$#@&*^|\\/~[]{}"))) >= 1):
            raise ValidationError(
                "Пароль должен содержать хотя бы 1 строчную и заглавную буквы латинского алфавита, цифру " \
                "и один знаков пунктуации или один из символов: %, $, #, @, &, *, ^, |, \\, /, ~, [, ], {, }")

        return True

    def check_email(self):
        if User.query.filter_by(email=self.email.data).first():
            return False
        return True

    def check_login(self):
        if User.query.filter_by(login=self.login.data).first():
            return False
        return True


class GoodsForm(FlaskForm):
    name = StringField('Название', validators=[data_required])
    description = TextAreaField('Описание', validators=[data_required])
    category = StringField('Категория', validators=[data_required])
    manufacturer = StringField('Производитель', validators=[data_required])
    price = IntegerField('Цена', validators=[data_required])
    photo = FileField('Фото', validators=[FileRequired()])
