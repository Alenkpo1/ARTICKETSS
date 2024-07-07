import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    mail = db.Column(db.String(255), nullable=False)
    contraseña = db.Column(db.String(255), nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    telefono = db.Column(db.String(255), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.now())

class Eventos(db.Model):
    __tablename__ = 'eventos'
    id = db.Column(db.Integer, primary_key=True)
    nombre_evento = db.Column(db.String(255), nullable=False)
    fecha = db.Column(db.String(255), nullable=False)
    hora = db.Column(db.String(255), nullable=False)
    lugar = db.Column(db.String(255), nullable=False)
    imagen = db.Column(db.String(255), nullable=False)


class Entradas(db.Model):
    __tablename__ = 'entradas'
    id = db.Column(db.Integer, primary_key=True)
    evento_id = db.Column(db.Integer, db.ForeignKey('eventos.id'))
    tipo_entrada = db.Column(db.String(255), nullable=False)
    precio = db.Column(db.Integer, nullable=False)
    cantidad_disponible = db.Column(db.Integer, nullable=False)

class Ventas(db.Model):
    __tablename__ = 'ventas'   
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    entrada_id = db.Column(db.Integer, db.ForeignKey('entradas.id'))
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_venta = db.Column(db.DateTime, default=datetime.datetime.now())
    total_pago = db.Column(db.Integer, nullable=False)