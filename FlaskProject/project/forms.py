from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FloatField
from wtforms.validators import Length, EqualTo, DataRequired, ValidationError
from project.models import Plant, Components

class RegisterForm(FlaskForm):

        def validate_username(self, username_to_check):
                user = Plant.query.filter_by(username=username_to_check.data).first()
                if user:
                        raise ValidationError('Пользователь с таким именем уже существует! Введите другое имя')
           
        username = StringField(label='Имя пользователя:', validators=[Length(min=2, max=30), DataRequired()])
        password1 = PasswordField(label='Пароль:', validators=[Length(min=6), DataRequired()])
        password2 = PasswordField(label='Подтвердите пароль:', validators=[EqualTo('password1'), DataRequired()])
        submit = SubmitField(label='Создать аккаунт')


class LoginForm(FlaskForm):

        username = StringField(label='Имя пользователя:', validators=[DataRequired()])
        password = PasswordField(label='Пароль:', validators=[DataRequired()])
        submit = SubmitField(label='Войти')

class AddComponentForm(FlaskForm):

        def validate_qrcode(self, qrcode_to_check):
                qrcode = Components.query.filter_by(qrcode=qrcode_to_check.data).first()
                if qrcode:
                        raise ValidationError('Деталь с таким QR-code уже существует! Введите другой QR-code')

        qrcode = StringField(label='QR-код', validators=[DataRequired()])
        ctype = SelectField(label='Выберите тип компонента', validators=[DataRequired()], choices=[])
        submit = SubmitField(label='Добавить')

class PowerSupplyTestingForm(FlaskForm):
        p = FloatField(label='Параметр', validators=[DataRequired()])
        submit = SubmitField(label='Отправить')

class PowerManagementModuleTestingForm(FlaskForm):
        p1 = FloatField(label='Параметр 1', validators=[DataRequired()])
        p2 = FloatField(label='Параметр 2', validators=[DataRequired()])
        p3 = FloatField(label='Параметр 3', validators=[DataRequired()])
        submit = SubmitField(label='Отправить')

class HandleTestingForm(FlaskForm):
        submit_success = SubmitField(label='Годен')
        submit_failure = SubmitField(label='Не годен')

class ComponentSearchForm(FlaskForm):
        search = StringField(label='QR-код', validators=[DataRequired()])
        submit = SubmitField(label='Добавить')