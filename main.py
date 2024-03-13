from flask import Flask, render_template, request, jsonify
from forms import UserForm
from flask import flash,redirect
from flask import g
from flask_wtf.csrf import CSRFProtect
from config import DevConfig
app = Flask(__name__)
from models import db
from forms import UserForm,EmpleadoForm,PizzeriaForm
from models import Alumnos,Empleados,Pizza,Cliente,detalle_pizza_compra,ventaFinal
import json
import datetime


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



@app.route('/ventasByDayOrMonth', methods=['POST'])
def ventasByDayOrMonth():
    dayOrMonth = request.json["dayOrMonth"]
    ventas = ventaFinal.query.all()

    days = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sabado": 5,
        "domingo": 6
    }

    mon = {
        "enero": 1,
        "febrero": 2,
        "marzo": 3,
        "abril": 4,
        "mayo": 5,
        "junio": 6,
        "julio": 7,
        "agosto": 8,
        "septiembre": 9,
        "octubre": 10,
        "noviembre": 11,
        "diciembre": 12
    }

    if dayOrMonth in days:
        ventas_filtradas = [venta_to_dict(venta) for venta in ventas if venta.fecha_compra.weekday() == days[dayOrMonth]]
        print(f"Ventas del dia: {ventas_filtradas}")
    else:
        ventas_filtradas = [venta_to_dict(venta) for venta in ventas if venta.fecha_compra.month == mon[dayOrMonth]]
        print(f"Ventas del mes: {ventas_filtradas}")

    total_ventas = sum([venta["total"] for venta in ventas_filtradas])
    return jsonify({"total_ventas": total_ventas, "ventas": ventas_filtradas})



def venta_to_dict(venta):
    return {
        "id": venta.id,
        "nombreCliente": venta.nombreCliente,
        "total": venta.total,
    }
    


@app.route('/pizza', methods=['GET', 'POST', 'DELETE', 'PUT'])
def pizza():
    pizzeria_form = PizzeriaForm(request.form)
    precio_pizza = {
        "chica": 40,
        "mediana": 80,
        "grande": 120
    }
    ventas = ventaFinal.query.all()
    
    ventas = [venta.__dict__ for venta in ventas if venta.fecha_compra.date() == datetime.datetime.now().date()]
    print(f"Ventas del dia: {ventas}")

    total_ventas = lambda ventas: sum([venta["total"] for venta in ventas])

    if request.method == 'PUT':
        
        id_cliente = request.json["id_cliente"]
        id_pizza = request.json["ids"]
        fecha = request.json["fecha"]
       
        pizzas=[]
       
        id_pizza = json.loads(id_pizza)

       
        for id_pizza in id_pizza:
                pizza = Pizza.query.filter_by(id=id_pizza).first()
                pizzas.append(pizza)

        pizzas = [pizza.__dict__ for pizza in pizzas]

        cliente = Cliente.query.filter_by(id=id_cliente).first()

        precio_Total =  0
        for pizza in pizzas:
                precio_Total += pizza["numPizzas"] * precio_pizza[pizza["tamanio"]] +(10 if pizza["jamon"] else 0) * pizza["numPizzas"] + (10 if pizza["pina"] else 0) * pizza["numPizzas"] + (10 if pizza["champinones"] else 0) * pizza["numPizzas"]

        

        venta = ventaFinal(nombreCliente=cliente.nombre, total=precio_Total, fecha_compra=fecha)
        db.session.add(venta)
        db.session.commit()

        
        pizzeria_form.process()

        return render_template('pizza.html', form=pizzeria_form, ventas=ventas, total_ventas=total_ventas(ventas))

    if request.method == 'DELETE':
        idsToDelete = request.json["idsToDelete"]
        id_cliente  = request.json["id_cliente"]
        print(f"idsToDelete: {idsToDelete} del id_cliente: {id_cliente}")
        
        idsToDelete = json.loads(idsToDelete)
        
        
        for id_pizza in idsToDelete:
                print(f"Eliminando pizza con id: {id_pizza}")
                
                detalle = detalle_pizza_compra.query.filter_by(id_cliente=id_cliente, id_pizza=id_pizza).first()
                db.session.delete(detalle)
                db.session.commit()
                pizza = Pizza.query.filter_by(id=id_pizza).first()
                db.session.delete(pizza)
                db.session.commit()
        pizzas = db.session.query(Pizza).join(detalle_pizza_compra).filter(detalle_pizza_compra.id_cliente == id_cliente).all()
        pizzas = [pizza.__dict__ for pizza in pizzas]
        pizzeria_form.id.data = id_cliente  
        
        for pizza in pizzas:
            pizza["subtotal"] =pizza["numPizzas"] * precio_pizza[pizza["tamanio"]] +(10 if pizza["jamon"] else 0) * pizza["numPizzas"] + (10 if pizza["pina"] else 0) * pizza["numPizzas"] + (10 if pizza["champinones"] else 0) * pizza["numPizzas"]
        return render_template('pizza.html', form=pizzeria_form, pizzas=pizzas, ventas=[], total_ventas=0)

    if request.method == 'POST' and pizzeria_form.validate():
        id_cliente = pizzeria_form.id.data
        if not id_cliente:  
            cliente = Cliente(nombre=pizzeria_form.Nombre.data, direccion=pizzeria_form.Direccion.data, telefono=pizzeria_form.Telefono.data)
            db.session.add(cliente)
            db.session.commit()
            id_cliente = cliente.id 

        print(f"Cliente: {id_cliente}")
        pizzeria_form.id.data = id_cliente
        

        pizza = Pizza(numPizzas=pizzeria_form.NumPizzas.data, tamanio=pizzeria_form.Tamanio.data, jamon=pizzeria_form.Jamon.data, pina=pizzeria_form.Pina.data, champinones=pizzeria_form.Champinones.data)
        db.session.add(pizza)
        db.session.commit()

        detalle = detalle_pizza_compra(id_cliente=id_cliente, id_pizza=pizza.id)
        db.session.add(detalle)
        db.session.commit()

        pizzas = db.session.query(Pizza).join(detalle_pizza_compra).filter(detalle_pizza_compra.id_cliente == id_cliente).all()
        pizzas = [pizza.__dict__ for pizza in pizzas]
        for pizza in pizzas:
            pizza["subtotal"] = pizza["numPizzas"] * precio_pizza[pizza["tamanio"]] +(10 if pizza["jamon"] else 0) * pizza["numPizzas"] + (10 if pizza["pina"] else 0) * pizza["numPizzas"] + (10 if pizza["champinones"] else 0) * pizza["numPizzas"]
        
        print(f"Las pizzas acumuladas son: {pizzas}")

        return render_template('pizza.html', form=pizzeria_form, pizzas=pizzas, ventas=[], total_ventas=0)


    return render_template('pizza.html', form=pizzeria_form, pizzas=[], ventas=ventas, total_ventas=total_ventas(ventas))

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



@app.route('/editar', methods=['GET', 'POST'])
def editar_empleado():
        form = EmpleadoForm(request.form)
        if request.method == 'GET':
                id = request.args.get('id')
                empleado = Empleados.query.filter_by(id=id).first()
                form.nombre.data = empleado.nombre
                form.dirección.data = empleado.dirección
                form.telefono.data = empleado.telefono
                form.correo.data = empleado.correo
                form.sueldo.data = empleado.sueldo
                return render_template('empleados.html', form=form)
        if request.method == 'POST':
                id = request.args.get('id')
                empleado = Empleados.query.filter_by(id=id).first()
                empleado.nombre = form.nombre.data
                empleado.dirección = form.dirección.data
                empleado.telefono = form.telefono.data
                empleado.correo = form.correo.data
                empleado.sueldo = form.sueldo.data
                db.session.commit()
                return redirect("/empleados/tabla")
        
@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar_empleado():
        form = EmpleadoForm(request.form)
        if request.method == 'GET':
                id = request.args.get('id')
                empleado = Empleados.query.filter_by(id=id).first()
                form.nombre.data = empleado.nombre
                form.dirección.data = empleado.dirección
                form.telefono.data = empleado.telefono
                form.correo.data = empleado.correo
                form.sueldo.data = empleado.sueldo
                form.id = empleado.id
                return render_template('empleados.html', form=form)
        if request.method == 'POST':
                id = request.args.get('id')
                empleado = Empleados.query.filter_by(id=id).first()
                db.session.delete(empleado)
                db.session.commit()
                return redirect("/empleados/tabla")
        




@app.route('/alumnos', methods=['GET', 'POST'])
def alumnos():
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
