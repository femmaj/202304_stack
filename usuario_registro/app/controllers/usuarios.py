from flask import render_template, request, redirect, session, flash, url_for
from app.models.usuario import Usuario
from app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app) 

@app.route('/')
def inicio():

    if 'usuario' not in session:
        return redirect(url_for ("login"))

    return render_template('usuario.html')

@app.route('/login')
def login():

    if 'usuario' in session:
        return redirect(url_for("inicio"))
    
    return render_template('auth/login.html')

@app.route('/procesar_login', methods=['POST'])
def procesar_login():

    usuario_encontrado = Usuario.get_by_email(request.form['email'])

    if not usuario_encontrado:
        flash('Existe un error en tu correo o contraseña', 'warning')
        return redirect(url_for("login"))

    login_seguro = bcrypt.check_password_hash(usuario_encontrado.password, request.form['password'])

    data = {
        "usuario_id": usuario_encontrado.id,
        "nombre": usuario_encontrado.nombre,
        "email": usuario_encontrado.email,
    }

    if login_seguro:
        session['usuario'] = data
        flash('Genial, pudiste entrar sin problemas!', 'success')

    else:
        flash('Existe un error en tu correo o contraseña', 'warning')
        return redirect(url_for("login"))

    return redirect(url_for("inicio"))

@app.route('/procesar_registro', methods=['POST'])
def procesar_registro():

    if request.form['password'] != request.form['confirm_password']:
        flash("La contraseña no es igual", "warning")
        return redirect(url_for("login"))
    
    if not Usuario.validar(request.form):
        return redirect(url_for("login"))

    password_hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'email': request.form['email'],
        'nombre': request.form['nombre'],
        'password': password_hash,
    }

    existe_usuario = Usuario.get_by_email(request.form['email'])
    if existe_usuario:
        flash("el correo ya está registrado.", "warning")
        return redirect(url_for("login"))


    resultado = Usuario.save(data)
    if resultado:
        flash("Te has registrado correrctamente", "success")
    else:
        flash("Errores", "danger")

    return redirect(url_for("login"))

@app.route('/salir')
def salir():
    session.clear()
    flash('Cerraste sesión sin problemas!', 'secondary')
    return redirect(url_for("login"))

