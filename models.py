from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()

class Alumnos(db.Model):
    __tablename__ = 'alumnos'
    id: int = db.Column(db.Integer, primary_key=True)
    nombre: str = db.Column(db.String(50))
    apaterno: str = db.Column(db.String(50))
    email: str = db.Column(db.String(50))
    created_at: datetime = db.Column(db.DateTime, default=datetime.datetime.now)


class Empleados(db.Model):
    __tablename__ = 'empleados'
    id: int = db.Column(db.Integer, primary_key=True)
    nombre: str = db.Column(db.String(50))
    dirección: str = db.Column(db.String(50))
    telefono: str = db.Column(db.String(50))
    correo: str = db.Column(db.String(50))
    sueldo: float = db.Column(db.Float)

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id: int = db.Column(db.Integer, primary_key=True)
    nombre: str = db.Column(db.String(50))
    direccion: str = db.Column(db.String(50))
    telefono: str = db.Column(db.String(50))
    fecha_compra: datetime = db.Column(db.DateTime, default=datetime.datetime.now)

class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id: int = db.Column(db.Integer, primary_key=True)
    numPizzas: int = db.Column(db.Integer)
    tamanio: str = db.Column(db.String(50))
    jamon: bool = db.Column(db.Boolean)
    pina: bool = db.Column(db.Boolean)
    champinones: bool = db.Column(db.Boolean)
    fecha_compra: datetime = db.Column(db.DateTime, default=datetime.datetime.now)


class detalle_pizza_compra(db.Model):
    __tablename__ = 'detalle_pizza_compra'
    id: int = db.Column(db.Integer, primary_key=True)
    id_cliente: int = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    id_pizza: int = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    fecha_compra: datetime = db.Column(db.DateTime, default=datetime.datetime.now)


class ventaFinal(db.Model):
    __tablename__ = 'ventaFinal'
    id: int = db.Column(db.Integer, primary_key=True)
    nombreCliente: str = db.Column(db.String(50))
    total: float = db.Column(db.Float)
    fecha_compra: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    dia = db.Column(db.String(50))
    mes = db.Column(db.String(50))
    anio = db.Column(db.String(50))



    
    


    