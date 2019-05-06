from flask import Flask, render_template, flash, redirect, url_for, session, request, logging  #render_template: para recargar la pagina
from clases import Clases
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
#from DBmodels import Gimnasio
#import jinja2
import os, sys
sys.path.insert(0, os.path.abspath(".."))


#from api.DBmodels import Gimnasio
from api import GymAPI

app = Flask(__name__)

Clases = Clases()

api = GymAPI.GymAPI()
nombre_usuario = ""
correo_usuario = "alex@gmail.com" #BORRAR

#Home para todos, pero de manera que cada quien pueda ver lo suyo
@app.route('/home')
def home():
    return render_template('home.html')

#Login page 
@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form['correo']
        input_password = request.form['password']
     
        usuarios = api.get_all_users()
        usuarios_array = []
        
        '''
        for i in range(len(usuarios)-1):
            usuarios_array.append(usuarios[i]['_id'])
            usuarios_array.append(usuarios[i]['Nombre_completo'])
            usuarios_array.append(usuarios[i]['email'])
        '''
        #print(usuarios)

        domain = email.rsplit('@', 1)[1]
        global correo_usuario
        correo_usuario = email
        #Comparar contrasenias
        password_redis = api.get_password_user(email)
        if email == "admin@mambafit.com": #para el administrador
            if sha256_crypt.verify(input_password, password_redis):
                session['admin'] = True
                session['nombre'] = 'Admin'
                return redirect(url_for('home'))
            else:
                error = 'Usuario no encontrado'
                app.logger.info('NO VALIDO')
                return render_template('login.html', error=error)
        if domain == 'mambafit.com': #para los instructores
            if sha256_crypt.verify(input_password, password_redis):
                session['instructor'] = True
                session['nombre'] = 'Instructor'
                
                result = api.get_all_instructors()
                print(result)
                return redirect(url_for('home'))
            else:
                error = 'Usuario no encontrado'
                return render_template('login.html', error=error)
        else:
            global nombre_usuario
            nombre_usuario = api.get_name_user(email)
            print(correo_usuario)
            if password_redis == False: #Not found
                error = 'Correo no encontrado'
                return render_template('login.html', error=error)
            else: 
                if sha256_crypt.verify(input_password, password_redis):
                    app.logger.info('VALIDO')
                    session['logged_in'] = True
                    session['nombre'] = nombre_usuario
                    return redirect(url_for('home'))
                else:
                    error = 'Usuario no encontrado'
                    app.logger.info('NO VALIDO')
                    return render_template('login.html', error=error)
    
    return render_template('login.html')

#Logout
@app.route('/logout')
def logout():
    session.clear()
    global nombre_usuario
    nombre_usuario = ""
    global correo_usuario
    correo_usuario = ""
    return redirect(url_for('login'))

#Apartado para saber el perfil de usuario
@app.route('/perfil')
def perfil():
    perfil_usuario = api.get_user(correo_usuario)
    print(perfil_usuario)
    nombre = perfil_usuario['Nombre_completo']
    direccion = perfil_usuario['Direccion']
    email = perfil_usuario['email']
    tarjeta = perfil_usuario['Tarjeta']['No_tarjeta']
    tarjeta = '*** ' + tarjeta[-4:]
    ID = perfil_usuario['ID']
    return render_template('perfil.html', name=nombre, address=direccion, correo=email, cuenta=tarjeta, id=ID)


#Apartado para saber la dieta del usuario
@app.route('/dieta')
def dieta():
    #comidas = api.get_food()
    #print(comidas)
    comida_usuario = api.get_food_user(correo_usuario)
    print(comida_usuario)
    nombre_comida = ""
    ingredientes = ""
    descripcion = ""
    
    nombre_comidas_array = []
    ingredientes_array = []
    descripcion_array = []
    tiene_comidas = False

    if comida_usuario is not None:
        for i in range(len(comida_usuario)):
            nombre_comida = comida_usuario[i]['Nombre_comida']
            ingredientes = comida_usuario[i]['Ingredientes']
            descripcion = comida_usuario[i]['Descripcion']

            nombre_comidas_array.append(nombre_comida)
            ingredientes_array.append(ingredientes)
            descripcion_array.append(descripcion)

            tiene_comidas = True
    else:
        tiene_comidas = False
    print(tiene_comidas)

    return render_template('dieta.html', tiene_comidas = tiene_comidas, nombre_comidas_array = nombre_comidas_array, ingredientes_array = ingredientes_array, descripcion_array = descripcion_array)

@app.route('/clases')
def clases():
    todas_clases = api.get_classes()
    nombre_todas_clases = []
    id_todas_clases = []
    nombre_todos_instructores = []
    horarios_todas_clases = []

    for i in range(len(todas_clases)):
        nombre_todas_clases.append(todas_clases[i]['Nombre'])
        id_todas_clases.append(todas_clases[i]['_id'])
        '''for x in range(len(todas_clases[i]['Instructores'])):
            nombre_todos_instructores.append(todas_clases[i]['Instructores'][x])
        for p in range(len(todas_clases[i]['Horarios'])):
            horarios_todas_clases.append(todas_clases[i]['Horarios'][p])'''
        #nombre_todos_instructores.append(todas_clases[i]['Instructores'])
        for x in range(len(todas_clases[i]['Instructores'])):
            coach = api.get_one_instructor(todas_clases[i]['Instructores'][x])
            nombre_coach = coach['Nombre_completo']
            nombre_todos_instructores.append(nombre_coach)
        horarios_todas_clases.append(todas_clases[i]['Horarios'])

    print(horarios_todas_clases)

    clases_usuario = api.get_classes_user(correo_usuario)
    id_horario = ""
    id_instructor = 0
    id_clase = ""
    horario_clase = ""
    nombre_clase = ""
    nombre_instructor = ""
    ubicacion_clase = ""
    clases_aux = []
    nombre_clases = []
    nombre_instructores = []
    horario_clases = []
    ubicacion_clases = []
    if clases_usuario is not None:

        if clases_usuario[0]['Horario'] != -1:
            for i in range(len(clases_usuario)):
                id_horario = str(clases_usuario[i]['Horario'])
                id_instructor = clases_usuario[i]['Instructor']
                id_clase = clases_usuario[i]['Id_clase']

                #Obtener la clase mediante el id
                clase_info = api.get_one_class(id_clase)
                print(clase_info)
                #Guardando la informacion de las clases del usuario
                horario_clase = clase_info['Horarios'][int(id_horario)] 
                #Obtener instructor
                nombre_instructor = "JUAN"
                nombre_clase = clase_info['Nombre']
                #obtener salon (primero redefinir la estructura de la bd.tabla clase)
                ubicacion_clase = "Salon 1"

                nombre_clases.append(nombre_clase)
                nombre_instructores.append(nombre_instructor)
                horario_clases.append(horario_clase)
                ubicacion_clases.append(ubicacion_clase)
                tiene_clases = True
        else:
            tiene_clases = False
    else:
        tiene_clases = False
        print("NO ENCONTRO USUARIO Y SUS CLASES DEBIDO A CORREO MALO")

    return render_template('clases.html', nombre_todas_clases = nombre_todas_clases, id_todas_clases = id_todas_clases, nombre_todos_instructores = nombre_todos_instructores, horarios_todas_clases = horarios_todas_clases, tiene_clases = tiene_clases, nombre_clases = nombre_clases, nombre_instructores = nombre_instructores, horario_clases = horario_clases, ubicacion_clases = ubicacion_clases)

class RegisterForm(Form):
    nombre = StringField('Nombre Completo', [
        validators.DataRequired(),
        validators.Length(min=5, max=50)]
        )
    direccion = StringField('Direccion', [
        validators.DataRequired(),
        validators.Length(min=5, max=50)]
        )
    no_tarjeta = StringField('No. Tarjeta', [
        validators.DataRequired(),
        validators.Length(min=16, max=16)]
        )
    csv_tarjeta = StringField('CSV', [
        validators.DataRequired(),
        validators.Length(min=3, max=3)]
        )
    titular_tarjeta = StringField('Titular de la tarjeta', [
        validators.DataRequired(),
        validators.Length(min=5, max=50)]
        )
    vencimiento_tarjeta = StringField('Vencimiento de la tarjeta', [
        validators.DataRequired(),
        validators.Length(min=5, max=5)]
        )
    correo = StringField('Correo', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirmar_contrasenia', message='No coincide las contrasenias')
    ])
    confirmar_contrasenia = PasswordField('Confirmar password')


@app.route('/register_users', methods=['GET', 'POST'])
def register_users():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        nombre = form.nombre.data
        direccion = form.direccion.data
        correo = form.correo.data
        csv = form.csv_tarjeta.data
        vencimiento = form.vencimiento_tarjeta.data
        no_tarjeta = form.no_tarjeta.data
        titular = form.titular_tarjeta.data

        password = sha256_crypt.encrypt(str(form.password.data))
        
        #GUARDAR EN LA BASE DE DATOS LOS DATOS INGRESADOS
        signup_redis = api.create_session(correo, password)
        if signup_redis == True:
            session['register'] = True
            signup_mongo = api.create_user(nombre, direccion, correo, no_tarjeta, titular, csv, vencimiento)
            return redirect(url_for('home'))
        else:
            error = "El correo que ingresaste se encuentra asociado a una cuenta"
            return render_template('register_users.html', form=form, error= error)
        

    return render_template('register_users.html', form=form)

class deleteForm(Form):
    correo = StringField('', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )

#Borrar a un usuario en especifico
@app.route('/delete_users', methods=['GET', 'POST'])
def delete_users():
    usuarios = api.get_all_users()
    nombres_usuarios = []
    correos_usuarios = []
    id_usuarios = []
    direcciones_usuarios = []

    for i in range(len(usuarios)):
        id_usuarios.append(usuarios[i]['ID'])
        nombres_usuarios.append(usuarios[i]['Nombre_completo'])
        correos_usuarios.append(usuarios[i]['email'])
        direcciones_usuarios.append(usuarios[i]['Direccion'])
    
    form = deleteForm(request.form)
    if request.method == 'POST':
        email_user = form.correo.data
        print(email_user)
        resultado_borrar = api.delete_user(email_user)
        if resultado_borrar == False:
            error = 'El correo que ingresaste no esta en la base de datos, vuelve a intentarlo'
            return render_template('delete_users.html', error = error, form = form, id_usuarios = id_usuarios, nombres_usuarios = nombres_usuarios, correos_usuarios = correos_usuarios, direcciones_usuarios = direcciones_usuarios)
        else:
            return redirect(url_for('home')) 
    return render_template('delete_users.html', form = form, id_usuarios = id_usuarios, nombres_usuarios = nombres_usuarios, correos_usuarios = correos_usuarios, direcciones_usuarios = direcciones_usuarios)
    
#Form para la dieta al crearla
class dietaForm(Form):
    nombre_comida = StringField('Nombre Comida:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )
    ingredientes = StringField('Ingredientes:', [
        validators.DataRequired(),
        validators.Length(min=3, max=500)]
        )
    descripcion = StringField('Descripcion:', [
        validators.DataRequired(),
        validators.Length(min=3, max=500)]
        )
    correo_cliente =  StringField('Correo del usuario:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )

#Para que el instructor pueda crear dietas
@app.route('/crear_dieta', methods=['GET', 'POST'])
def crear_dieta():
    form = dietaForm(request.form)
    if request.method == 'POST' and form.validate():
        nombre_comida = form.nombre_comida.data
        ingredientes = form.ingredientes.data
        descripcion = form.descripcion.data
        correo_cliente = form.correo_cliente.data

        signup_redis = api.get_password_user(correo_cliente)
        if signup_redis:
            dieta = api.crear_dieta(nombre_comida, ingredientes, descripcion, correo_cliente)
            return redirect(url_for('home'))
        else:
            error = "No existe correo que ingresaste"
            return render_template('crear_dieta.html', form=form, error= error)
        
    return render_template('crear_dieta.html', form = form)

#Form para crear una clase
class claseForm(Form):
    nombre_clase = StringField('Nombre Clase:', [
        validators.DataRequired(),
        validators.Length(min=2, max=50)]
        )
    id_clase = StringField('Clase ID:', [
        validators.DataRequired(),
        validators.Length(min=1, max=500)]
        )
    instructores = StringField('Instructores:', [
        validators.DataRequired(),
        validators.Length(min=1, max=500)]
        )
    horarios =  StringField('Horarios Clase:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )

#Crear una clase desde el instructor
@app.route('/crear_clase', methods=['GET', 'POST'])
def crear_clase():
    print(api.get_classes())
    form = claseForm(request.form)
    if request.method == 'POST' and form.validate():
        nombre_clase = form.nombre_clase.data
        #CAMBIAR PARA QUE SE GENERE INCREMENTAL EL ID_CLASE
        id_clase = form.id_clase.data
        instructores = form.instructores.data
        horarios = form.horarios.data
        instructor = api.get_one_instructor(correo_usuario)
        #id_instructor = instructor['ID_Instructor'] REGRESAAAAR
        id_instructor = 'I00001'
        instructor_inscrito = False

        clase_ya_creada = api.get_one_class(id_clase)
        if clase_ya_creada is False:
            #Crear clase o aniadir el instructor a ella
            clase = api.create_class(nombre_clase, id_clase, id_instructor, horarios)
            return redirect(url_for('home'))
        else:
            msg = "Ya esta creada la clase, por lo que haz ingresado en ella como instructor"
            print("Ya esta creada la clase, por lo que haz ingresado en ella como instructor")
            for i in range(len(clase_ya_creada['Instructores'])):
                if clase_ya_creada['Instructores'][i] == id_instructor:
                    instructor_inscrito = True
            if instructor_inscrito is not True: #Si no esta el instructor
                clase = api.insert_class_instructor_schedule(id_clase, id_instructor, horarios)
            else:
                clase = api.insert_class_schedule(id_clase, horarios)
            return render_template('crear_clase.html', form=form, msg = msg)
        
    return render_template('crear_clase.html', form = form)



if __name__ == "__main__":
    app.secret_key='12345'
    app.run(debug=True)