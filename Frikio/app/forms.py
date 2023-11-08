from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Registrarse')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Ingresar')


class DomicilioForm(FlaskForm):
    nombre = StringField('Nombre y Apellido', validators=[DataRequired(), Length(max=64)])
    direccion = StringField('Direccion', validators=[DataRequired(), Length(max=64)])
    ciudad = StringField('Ciudad', validators=[DataRequired(), Length(max=64)])
    cp = StringField('Código Postal', validators=[DataRequired(), Length(max=32)])
    provincia = StringField('Provincia', validators=[DataRequired(), Length(max=64)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=32)])
    submit = SubmitField('Continuar en Metodo de pago')
