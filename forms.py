
from flask_wtf import Form
from wtforms import StringField, IntegerField, EmailField
# importamos los validadores de WTForms
from wtforms.validators import DataRequired, Length, Email



class UserForm(Form):
    nombre = StringField('nombre',validators=[DataRequired(message="El campo es requerido"), Length(4, 10, "Ingresa un nombre valido")])
    a_paterno = StringField('apaterno', validators=[DataRequired(message="El campo es requerido")])
    id = StringField('id', validators=[Length(4, 20, "Ingresa un id valido min 4 max 20"), DataRequired(message="El campo es requerido")])
    edad = IntegerField('edad', validators=[DataRequired(message="El campo es requerido")])
    email = EmailField('email', validators=[DataRequired(message="El campo es requerido"), Email(message="Ingresa un email valido")])