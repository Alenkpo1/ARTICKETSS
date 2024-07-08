from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, send_file
from time import sleep
from models import db, Usuarios, Eventos, Entradas, Carrito, Contacto

app = Flask(__name__)
port = 5000

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://articket:articket@localhost:5432/artickets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/index')
def index():
    return render_template('index.html')

#Retorna la imagen de un evento específico.
@app.route('/imagenes_eventos/<image_id>')
def imagenes_eventos(image_id):
    img = Eventos.query.get(image_id)
    return send_file(img.imagen, mimetype='image/png')

@app.route('/home/<nombre_usuario>')
def home(nombre_usuario):
    return render_template('home.html', nombre_usuario=nombre_usuario)

@app.route('/contact/<nombre_usuario>', methods=['POST', 'GET'])
def contact(nombre_usuario):
    if request.method == 'GET':
        return render_template('contact.html', nombre_usuario=nombre_usuario)  #Renderiza el formulario de contacto.
    if request.method == 'POST':
        nombre = request.form['name']
        email = request.form['email']
        mensaje = request.form['message']
        nuevo_contacto = Contacto(
            nombre=nombre,
            email=email,
            mensaje=mensaje
        )
        db.session.add(nuevo_contacto)  #Guarda el nuevo contacto en la base de datos.
        db.session.commit()
        return "Contacto enviado"

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  #Renderiza el formulario de login.
    if request.method == 'POST':
        mail = request.form['mail']
        contraseña = request.form['contraseña']
        if not Usuarios.query.filter_by(mail=mail, contraseña=contraseña).all():
            print('Credenciales incorrectas')
            return redirect(url_for('login'))
        nombre = Usuarios.query.filter_by(mail=mail, contraseña=contraseña).first().nombre
        if Usuarios.query.filter_by(mail=mail, contraseña=contraseña).all():
            return redirect(url_for('home', nombre_usuario=nombre))  #Redirige al usuario a la página de inicio.

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')  #Renderiza el formulario de registro.
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        mail = request.form['mail']
        contraseña = request.form['contraseña']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        if Usuarios.query.filter_by(mail=mail).all():
            print('Ya existe un usuario con ese correo')
            return redirect(url_for('register'))  #Redirige de vuelta al formulario de registro.
        else:
            #Crea un nuevo usuario y lo añade a la base de datos.
            usuario = Usuarios(nombre=nombre, apellido=apellido, mail=mail, contraseña=contraseña, direccion=direccion, telefono=telefono)
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('login'))

@app.route('/about/<nombre_usuario>')
def about(nombre_usuario):
    return render_template('about.html', nombre_usuario=nombre_usuario)

@app.route('/cuenta/<nombre_usuario>', methods=['POST', 'GET'])
def cuenta(nombre_usuario):
    if request.method == 'GET':
        return render_template('cuenta.html', nombre_usuario=nombre_usuario)  #Renderiza la página de cuenta.
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        mail = request.form['mail']
        contraseña = request.form['contraseña']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        cuenta = Usuarios.query.filter_by(mail=mail).first()
        cuenta.nombre = nombre
        cuenta.apellido = apellido
        cuenta.mail = mail
        cuenta.contraseña = contraseña
        cuenta.direccion = direccion
        cuenta.telefono = telefono
        db.session.commit()  #Guarda los cambios en los detalles de la cuenta.
        return redirect(url_for('cuenta', nombre_usuario=nombre))

@app.route('/cuenta/detalle/<nombre_usuario>')
def cuenta_detalle(nombre_usuario):
    try:
        cuenta = Usuarios.query.filter_by(nombre=nombre_usuario).first()
        cuenta_data = {
            'nombre': cuenta.nombre,
            'apellido': cuenta.apellido,
            'mail': cuenta.mail,
            'contraseña': cuenta.contraseña,
            'direccion': cuenta.direccion,
            'telefono': cuenta.telefono
        }
        return jsonify(cuenta_data)  #Retorna los detalles de la cuenta del usuario en formato JSON.
    except:
        return jsonify({"mensaje": "La cuenta no existe"})

@app.route('/faq/<nombre_usuario>')
def faq(nombre_usuario):
    return render_template('faq.html', nombre_usuario=nombre_usuario)

@app.route('/eventos/<nombre_usuario>')
def eventos(nombre_usuario):
    return render_template('eventos.html', nombre_usuario=nombre_usuario)

@app.route('/evento')
def evento():
    try:
        eventos = Eventos.query.all()
        eventos_data = []
        for evento in eventos:
            evento_data = {
                'id': evento.id,
                'nombre_evento': evento.nombre_evento,
                'fecha': evento.fecha,
                'hora': evento.hora,
                'lugar': evento.lugar
            }
            eventos_data.append(evento_data)
        return jsonify(eventos_data)  #Retorna detalles de todos los eventos en formato JSON.
    except:
        return jsonify({"mensaje": "No existen eventos"})  #Mensaje de error si no hay eventos registrados.

@app.route('/evento_lugar/<lugar>')
def evento_lugar(lugar):
    try:
        eventos = Eventos.query.filter_by(lugar=lugar)
        eventos_data = []
        for evento in eventos:
            evento_data = {
                'id': evento.id,
                'nombre_evento': evento.nombre_evento,
                'descripcion': evento.descripcion,
                'fecha': evento.fecha,
                'hora': evento.hora,
                'lugar': evento.lugar
            }
            eventos_data.append(evento_data)
        return jsonify(eventos_data)  #Retorna detalles de eventos en un lugar específico en formato JSON.
    except:
        return jsonify({"mensaje": "No existen eventos en esta ubicación"})  #Mensaje de error si no hay eventos en esa ubicación.

@app.route('/evento/<id_evento>')
def detalles_evento(id_evento):
    try:
        evento = Eventos.query.get(id_evento)
        evento_data = {
            'id': evento.id,
            'nombre_evento': evento.nombre_evento,
            'descripcion': evento.descripcion,
            'fecha': evento.fecha,
            'hora': evento.hora,
            'lugar': evento.lugar
        }
        return jsonify(evento_data)  #Retorna detalles de un evento específico en formato JSON.
    except:
        return jsonify({"mensaje": "El evento no existe"})  #Mensaje de error si el evento no existe.

@app.route('/carrito/agregar/<nombre_usuario>/<precio_entrada>/<id_entrada>')
def carrito_agregar(nombre_usuario, precio_entrada, id_entrada):
    nombre = nombre_usuario
    precio = precio_entrada
    id_entrada = id_entrada
    id_usuario = Usuarios.query.filter_by(nombre=nombre).first().id
    restante = Entradas.query.filter_by(id=id_entrada).first().cantidad_disponible
    if restante > 0:
        Entradas.query.filter_by(id=id_entrada).first().cantidad_disponible - 1
        carrito = Carrito(usuario_id=id_usuario, entrada_id=id_entrada, cantidad=1, precio=precio)
        db.session.add(carrito)  #Añade la entrada al carrito en la base de datos.
        db.session.commit()  #Guarda los cambios en la base de datos.
        return "Subido al carrito"
    else:
        return "No hay más entradas disponibles"

@app.route('/carrito/detalles/<nombre_usuario>')
def carrito_detalles(nombre_usuario):
    return render_template('carrito.html', nombre_usuario=nombre_usuario)  #Renderiza la página de detalles del carrito.

@app.route('/carrito/limpiar/<nombre_usuario>/<id_venta>', methods=['DELETE'])
def carrito_limpiar(nombre_usuario, id_venta):
    try:
        Carrito.query.filter_by(id=id_venta).delete()  #Elimina un ítem del carrito por su ID.
        db.session.commit()  #Guarda los cambios en la base de datos.
        return jsonify({'message': 'Ítem eliminado del carrito'}), 200
    except Exception as e:
        return jsonify({'message': 'Error al eliminar el ítem', 'error': str(e)}), 500

@app.route('/carrito/<nombre_usuario>')
def carrito(nombre_usuario):
    id_usuario = Usuarios.query.filter_by(nombre=nombre_usuario).first().id
    try:
        entradas = Carrito.query.filter_by(usuario_id=id_usuario).all()
        entradas_data = []
        for entrada in entradas:
            entrada_data = {
                'id': entrada.id,
                'usuario_id': entrada.usuario_id,
                'entrada_id': entrada.entrada_id,
                'precio': entrada.precio,
                'cantidad': entrada.cantidad
            }
            entradas_data.append(entrada_data)
        return jsonify(entradas_data)  #Retorna los detalles del carrito del usuario en formato JSON.
    except:
        return jsonify({"mensaje": "El carrito está vacío"})

@app.route('/eventos/detalles/<id_evento>/<nombre_usuario>')
def detalles(nombre_usuario, id_evento):
    return render_template('detalles.html', nombre_usuario=nombre_usuario, id_evento=id_evento)  #Renderiza la página de detalles de un evento.

@app.route('/seleccion/evento/<fecha_evento>/<nombre_usuario>')
def seleccion_fecha(nombre_usuario):
    return render_template('login.html', nombre_usuario=nombre_usuario)  #Renderiza la página de selección de fecha de evento.

@app.route('/seleccion/evento/<asiento_evento>/<nombre_usuario>')
def seleccion_asiento(nombre_usuario):
    return render_template('login.html', nombre_usuario=nombre_usuario)  #Renderiza la página de selección de asiento de evento.

@app.route('/entradas/<id_evento>')
def entrada(id_evento):
    try:
        entradas = Entradas.query.filter_by(evento_id=id_evento)
        entradas_data = []
        for entrada in entradas:
            entrada_data = {
                'id': entrada.id,
                'evento_id': entrada.evento_id,
                'tipo_entrada': entrada.tipo_entrada,
                'precio': entrada.precio,
                'cantidad_disponible': entrada.cantidad_disponible,
            }
            entradas_data.append(entrada_data)
        return jsonify(entradas_data)  #Retorna las entradas disponibles para un evento en formato JSON.
    except:
        return jsonify({"mensaje": "El evento no tiene entradas"})

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()  #Crea todas las tablas en la base de datos si no existen.
    app.run(host='0.0.0.0', debug=True, port=port)  # Ejecuta Flask en el puerto seleccionado.