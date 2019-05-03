from flask import Flask, render_template, flash, redirect, url_for, session, request, logging  #render_template: para recargar la pagina
from clases import Clases
#from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm

app = Flask(__name__)

Clases = Clases()

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        mail = request.form['correo']
        input_password = request.form['password']
        
        #Obtener contrasenia de redis
        given_mail_password = '$5$rounds=535000$spHDz1JwXJin4J9f$8WKfK1I1raeQW5K0olDa.djJ4ESnaqm5fLzPTJKad70'

        #Comparar contrasenias
        #BORRAR
        if mail == "alex@gmail":
            app.logger.info('VALIDO')
            session['logged_in'] = True
            session['nombre'] = mail #CAMBIAR A EL NOMBRE DEL USUARIO QUE SE LOGEO
            return redirect(url_for('home'))
        else:
            app.logger.info('NO VALIDO')
            error = 'Usuario no encontrado'
            return render_template('login.html', error=error)

        #BORRAR

        '''
        if sha256_crypt.verify(input_password, given_mail_password):
            app.logger.info('VALIDO')
        else:
            app.logger.info('NO VALIDO')
        '''

    return render_template('login.html')

#Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/dieta')
def dieta():
    return render_template('dieta.html', clases = Clases)

@app.route('/clases')
def clases():
    return render_template('clases.html', clases = Clases)

class RegisterForm(Form):
    nombre = StringField('Nombre', [
        validators.DataRequired(),
        validators.Length(min=5, max=50)]
        )
    correo = StringField('Correo', [
        validators.DataRequired(),
        validators.Length(min=5, max=50)]
        )
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirmar_contrasenia', message='No coincide las contrasenias')
    ])
    
    confirmar_contrasenia = PasswordField('Confirmar password')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        correo = form.correo.data
        password = sha256_crypt.encrypt(str(form.password.data))
        print(nombre)
        flash('Registrado satisfactoriamente', 'success')

        session['register'] = True

        #GUARDAR EN LA BASE DE DATOS LOS DATOS INGRESADOS

        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.secret_key='12345'
    app.run(debug=True)