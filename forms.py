
from flask_wtf import Form
from wtforms import StringField, IntegerField, EmailField,FloatField,RadioField,BooleanField,SelectField,DateField
# importamos los validadores de WTForms
from wtforms.validators import DataRequired, Length, Email


class UserForm(Form):
    nombre = StringField('nombre',validators=[DataRequired(message="El campo es requerido"), Length(4, 10, "Ingresa un nombre valido")])
    a_paterno = StringField('apaterno', validators=[DataRequired(message="El campo es requerido")])
    id = StringField('id', validators=[Length(4, 20, "Ingresa un id valido min 4 max 20"), DataRequired(message="El campo es requerido")])
    edad = IntegerField('edad', validators=[DataRequired(message="El campo es requerido")])
    email = EmailField('email', validators=[DataRequired(message="El campo es requerido"), Email(message="Ingresa un email valido")])

class EmpleadoForm(Form):    
    id = StringField('id')
    nombre = StringField('nombre',validators=[DataRequired(message="El campo es requerido"), Length(4, 50, "Ingresa un nombre valido")])
    dirección = StringField('direccion', validators=[DataRequired(message="El campo es requerido")])
    telefono = StringField('telefono', validators=[Length(4, 50, "Ingresa un telefono valido min 4 max 50"), DataRequired(message="El campo es requerido")])
    correo = EmailField('correo', validators=[DataRequired(message="El campo es requerido"), Email(message="Ingresa un email valido")])
    sueldo = FloatField('sueldo', validators=[DataRequired(message="El campo es requerido")])


class PizzeriaForm(Form):
    id = StringField('id')
    Nombre = StringField('nombre',validators=[DataRequired(message="El campo es requerido"), Length(4, 50, "Ingresa un nombre valido")])
    Direccion = StringField('direccion', validators=[DataRequired(message="El campo es requerido")])
    fecha = DateField('fecha', validators=[DataRequired(message="El campo es requerido")])
    Telefono = StringField('telefono', validators=[Length(4, 50, "Ingresa un telefono valido min 4 max 50"), DataRequired(message="El campo es requerido")])
    NumPizzas = IntegerField('numPizzas', validators=[DataRequired(message="El campo es requerido")])
    Tamanio = RadioField('tamanio', choices=[('chica', 'Chica $40'), ('mediana', 'Mediana $80'), ('grande', 'Grande $120')], validators=[DataRequired(message="El campo es requerido")], default='chica')
    Jamon = BooleanField('Jamón $10', default=False)
    Pina = BooleanField('Piña $10', default=False)
    Champinones = BooleanField('Champiñones $10', default=False)
