from flask import Flask, render_template, request
from forms import UserForm
from flask import flash,redirect
from flask import g
from flask_wtf.csrf import CSRFProtect
from config import DevConfig
app = Flask(__name__)
from models import db
from forms import UserForm,EmpleadoForm
from models import Alumnos,Empleados



app.config.from_object(DevConfig)
csrf = CSRFProtect(app)


@app.route('/', methods=['GET', 'POST'])
def index():
        usuario_form = UserForm(request.form)
        if request.method == 'POST' and usuario_form.validate():
                try:
                        alumno = Alumnos(nombre=usuario_form.nombre.data, apaterno=usuario_form.a_paterno.data, email=usuario_form.email.data)
                        db.session.add(alumno)
                        db.session.commit()
                        print("Alumno guardado")
                except Exception as e:
                        print(f"Error en la base de datos: {e}")
                        db.session.rollback()                        
        return render_template('index.html', form=usuario_form)


@app.route('/empleados', methods=['GET', 'POST'])
def empleados():
        empleado_form = EmpleadoForm(request.form)
        if request.method == 'POST' and empleado_form.validate():
                try:
                        empleado = Empleados(nombre=empleado_form.nombre.data, dirección=empleado_form.dirección.data, telefono=empleado_form.telefono.data, correo=empleado_form.correo.data, sueldo=empleado_form.sueldo.data)
                        print(empleado)
                        db.session.add(empleado)
                        db.session.commit()
                        print("Empleado guardado")
                        return redirect("/empleados/tabla")
                except Exception as e:
                        print(f"Error en la base de datos: {e}")
                        db.session.rollback()                        
        return render_template('empleados.html', form=empleado_form)

@app.route('/empleados/tabla', methods=['GET'])
def tabla_empleados():
        empleados = Empleados.query.all()
        return render_template('tabla_empleado.html', empleados=empleados)



@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
        # titulo = "UTL!!!"
        # nombres = ["Mario", "Juan", "Pedro", "Dario"]
        # return render_template('alumnos.html', titulo=titulo, nombres=nombres)
        usuario_form = UserForm(request.form)
        nombre = None
        p_apellido = None
        m_apellido = None
        edad = None
        email = None


        if request.method == 'POST' and usuario_form.validate():
                nombre = usuario_form.nombre.data
                m_apellido = usuario_form.a_materno.data
                p_apellido = usuario_form.a_paterno.data
                edad = usuario_form.edad.data
                email = usuario_form.email.data

                print(f"Nombre: {nombre} {p_apellido} {m_apellido} Edad: {edad} Email: {email}")

                msj_flash = f"Bienvenido {g.nombre}"
                flash(msj_flash)
        return render_template('alumnos.html', form=usuario_form, nombre=nombre, p_apellido=p_apellido , m_apellido=m_apellido, edad=edad, email=email if email else "Email")
		

@app.errorhandler(404)
def error(error):
		return render_template('404.html', error = error), 404
   


if __name__ == '__main__':
        csrf.init_app(app)
        db.init_app(app)            
        with app.app_context():
                db.create_all()
        app.run(debug=True)
