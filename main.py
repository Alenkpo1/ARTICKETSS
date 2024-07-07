from flask import Flask, render_template, redirect, url_for, request, jsonify, flash, send_file
from time import sleep
from models import db, Usuarios, Eventos, Entradas, Ventas
app= Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://articket:articket@localhost:5432/artickets'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/imagenes_eventos/<image_id>')
def imagenes_eventos(image_id):
    img = Eventos.query.get(image_id)
    return send_file(img.imagen, mimetype='image/png')

@app.route('/home/<nombre_usuario>')
def home(nombre_usuario):
    return render_template('home.html', nombre_usuario=nombre_usuario)

@app.route('/login', methods= ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        mail = request.form['mail']
        contraseña = request.form['contraseña']
        nombre = Usuarios.query.filter_by(mail=mail, contraseña=contraseña).first().nombre
        if Usuarios.query.filter_by(mail=mail, contraseña=contraseña).all():
            return redirect(url_for('home', nombre_usuario=nombre))
        else:
            print('Credenciales incorrectas')
            return redirect(url_for('login'))

@app.route('/register', methods= ['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        mail = request.form['mail']
        contraseña = request.form['contraseña']
        direccion = request.form['direccion']
        telefono = request.form['telefono']

        if Usuarios.query.filter_by(mail=mail).all():
            print('Ya existe un usuario con ese correo')   
            return redirect(url_for('register'))
        else: 
            usuario = Usuarios(nombre=nombre, apellido=apellido, mail=mail, contraseña=contraseña, direccion=direccion, telefono=telefono)
            db.session.add(usuario)
            db.session.commit()
            return redirect(url_for('login'))
        
    
@app.route('/about/<nombre_usuario>')
def about(nombre_usuario):
    return render_template('about.html', nombre_usuario=nombre_usuario)

@app.route('/contact/<nombre_usuario>')
def contact(nombre_usuario):
    return render_template('contact.html', nombre_usuario=nombre_usuario)

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
        return jsonify(eventos_data)
    except:
        return jsonify({"mensaje":"No existen eventos"})
    
@app.route('/evento/<lugar>')
def evento_lugar(lugar):
    try:
        evento = Eventos.query.filter_by(lugar=lugar)
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
        return jsonify(eventos_data)
    except:
        return jsonify({"mensaje":"No existen eventos en esta ubicacion"})
    
@app.route('/evento/<id_evento>')
def detalles_evento(id_evento):
    try:
        evento = Eventos.query.get(id_evento)
        evento_data = {
            'id': evento.id,
            'nombre_evento': evento.nombre_evento,
            'fecha': evento.fecha,
            'hora': evento.hora,
            'lugar': evento.lugar
        }
        return jsonify(evento_data)
    except:
        return jsonify({"mensaje":"El evento no existe"})


@app.route('/eventos/detalle/<id_evento>/<nombre_usuario>')
def detalle(nombre_usuario, id_evento):
    
    return id_evento

@app.route('/seleccion/evento/<fecha_evento>/<nombre_usuario>')
def seleccion_fecha(nombre_usuario):
    return render_template('login.html', nombre_usuario=nombre_usuario)
@app.route('/seleccion/evento/<asiento_evento>/<nombre_usuario>')
def seleccion_asiento(nombre_usuario):
    return render_template('login.html', nombre_usuario=nombre_usuario)



if __name__=='__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True, port=port)