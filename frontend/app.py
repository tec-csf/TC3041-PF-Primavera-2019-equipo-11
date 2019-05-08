# -*- coding: utf-8 -*-
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging  #render_template: para recargar la pagina
from clases import Clases
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
#from DBmodels import Gimnasio
#import jinja2
import os, sys
import json
sys.path.insert(0, os.path.abspath(".."))


#from api.DBmodels import Gimnasio
from api import GymAPI

app = Flask(__name__)

Clases = Clases()

api = GymAPI.GymAPI()
nombre_usuario = ""
correo_usuario = "daniel@gmail.com" #BORRAR
logged_in_admin = False
logged_in_user = False
logged_in_instructor = False

#Home para todos, pero de manera que cada quien pueda ver lo suyo
@app.route('/')
def root():
    return redirect(url_for('login'))

#Home para todos, pero de manera que cada quien pueda ver lo suyo
@app.route('/home')
def home():
    if logged_in_admin or logged_in_user or logged_in_instructor:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

#Login page 
@app.route('/login', methods=['GET', 'POST'])
def login():
    #print(api.get_all_instructors())
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
        print(password_redis)
        if email == "admin@mambafit.com": #para el administrador
            if sha256_crypt.verify(input_password, password_redis):
                session['admin'] = True
                session['nombre'] = 'Admin'
                global logged_in_admin
                logged_in_admin = True
                return redirect(url_for('home'))
            else:
                error = 'Usuario no encontrado'
                app.logger.info('NO VALIDO')
                return render_template('login.html', error=error)
        if domain == 'mambafit.com': #para los instructores
            if password_redis is not False: #Not found
                if sha256_crypt.verify(input_password, password_redis):
                    session['instructor'] = True
                    session['nombre'] = 'Instructor'
                    global logged_in_instructor
                    logged_in_instructor = True
                    return redirect(url_for('home'))
                else:
                    error = 'Usuario no encontrado'
                    return render_template('login.html', error=error)
            else: 
                error = 'Correo no encontrado'
                return render_template('login.html', error=error)
        else:
            global nombre_usuario
            nombre_usuario = api.get_name_user(email)
            #print(correo_usuario)
            if password_redis == False: #Not found
                error = 'Correo no encontrado'
                return render_template('login.html', error=error)
            else: 
                if sha256_crypt.verify(input_password, password_redis):
                    app.logger.info('VALIDO')
                    session['logged_in'] = True
                    session['nombre'] = nombre_usuario
                    global logged_in_user
                    logged_in_user = True
                    return redirect(url_for('home'))
                else:
                    error = 'Usuario no encontrado'
                    app.logger.info('NO VALIDO')
                    return render_template('login.html', error=error)
    
    print(api.get_all_users())
    return render_template('login.html')

#Logout
@app.route('/logout')
def logout():
    session.clear()
    global nombre_usuario
    nombre_usuario = ""
    global correo_usuario
    correo_usuario = ""
    global logged_in_admin
    logged_in_admin = False
    global logged_in_user
    logged_in_user = False
    global logged_in_instructor
    logged_in_instructor = False
    return redirect(url_for('login'))

#Apartado para saber el perfil de usuario
@app.route('/perfil')
def perfil():
    if logged_in_user:
        perfil_usuario = api.get_user(correo_usuario)
        nombre = perfil_usuario['Nombre_completo']
        direccion = perfil_usuario['Direccion']
        email = perfil_usuario['email']
        tarjeta = perfil_usuario['Tarjeta']['No_tarjeta']
        tarjeta = '*** ' + tarjeta[-4:]
        ID = perfil_usuario['ID']
        return render_template('perfil.html', name=nombre, address=direccion, correo=email, cuenta=tarjeta, id=ID)
    else:
        return redirect(url_for('login'))


#Apartado para saber la dieta del usuario
@app.route('/dieta')
def dieta():
    if logged_in_user:
        #comidas = api.get_food()
        #print(comidas)
        comida_usuario = api.get_food_user(correo_usuario)
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

        return render_template('dieta.html', tiene_comidas = tiene_comidas, nombre_comidas_array = nombre_comidas_array, ingredientes_array = ingredientes_array, descripcion_array = descripcion_array)
    else:
        return redirect(url_for('login'))
    

@app.route('/clases')
def clases():
    if logged_in_user:
        todas_clases = api.get_classes()
        nombre_todas_clases = []
        id_todas_clases = []
        nombre_todos_instructores = []
        horarios_todas_clases = []
        aux_nombre_instructores = []
        aux_horarios = [] 

        for i in range(len(todas_clases)):
            print('Debug')
            print(todas_clases[i]['Cancelada'])
            if int(todas_clases[i]['Cancelada']) == 0:
                nombre_todas_clases.append(todas_clases[i]['Nombre'])
                id_todas_clases.append(todas_clases[i]['_id'])
                '''for x in range(len(todas_clases[i]['Instructores'])):
                    nombre_todos_instructores.append(todas_clases[i]['Instructores'][x])
                for p in range(len(todas_clases[i]['Horarios'])):
                    horarios_todas_clases.append(todas_clases[i]['Horarios'][p])'''
                #nombre_todos_instructores.append(todas_clases[i]['Instructores'])
                for x in range(len(todas_clases[i]['Instructores'])):
                    coach = api.get_one_instructor_id(todas_clases[i]['Instructores'][x])
                    nombre_coach = coach['Nombre_completo']
                    correo_coach = coach['email']
                    nombre_coach = ' ' + nombre_coach + ' (' + correo_coach + ') '
                    #print(nombre_coach)
                    aux_nombre_instructores.append(nombre_coach)
                #[x.encode('utf-8') for x in aux_nombre_instructores]
                #print(aux_nombre_instructores)
                #aux_nombre_instructores = [r.encode('utf-8') for r in aux_nombre_instructores]
                aux_nombre_instructores = ', '.join(map(str, aux_nombre_instructores))
                nombre_todos_instructores.append(aux_nombre_instructores)
                #print(nombre_todos_instructores)
                aux_nombre_instructores = []
                for p in range(len(todas_clases[i]['Horarios'])):
                    hors = todas_clases[i]['Horarios'][p]
                    hors = ' ' + hors + ' (' + str(p) + ') '
                    aux_horarios.append(hors)
                aux_horarios = ', '.join(map(str, aux_horarios))
                horarios_todas_clases.append(aux_horarios)
                aux_horarios= []


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
                    print(clases_usuario[i])
                    
                    id_horario = str(clases_usuario[i]['Horario'])
                    id_instructor = clases_usuario[i]['Instructor']
                    id_clase = clases_usuario[i]['Id_clase']

                    #Obtener la clase mediante el id
                    clase_info = api.get_one_class(id_clase)
                    print(clase_info)
                    #Guardando la informacion de las clases del usuario
                    horario_clase = clase_info['Horarios'][int(id_horario)] 
                    #Obtener instructor
                    id_instructor_str = clase_info['Instructores'][int(id_instructor)] 
                    info_instructor = api.get_one_instructor_id(id_instructor_str)
                    nombre_instructor = info_instructor['Nombre_completo']
                    nombre_clase = clase_info['Nombre']
                    #obtener salon (primero redefinir la estructura de la bd.tabla clase)

                    ubicacion_clase = clase_info['Ubicacion']

                    if int(clase_info['Cancelada']) == 0:
                        nombre_clases.append(nombre_clase)
                        nombre_instructores.append(nombre_instructor)
                        horario_clases.append(horario_clase)
                        ubicacion_clases.append(ubicacion_clase)
                        tiene_clases = True
                if len(nombre_clases) == 0:
                    tiene_clases = False
            else:
                tiene_clases = False
        else:
            tiene_clases = False

        return render_template('clases.html', nombre_todas_clases = nombre_todas_clases, id_todas_clases = id_todas_clases, nombre_todos_instructores = nombre_todos_instructores, horarios_todas_clases = horarios_todas_clases, tiene_clases = tiene_clases, nombre_clases = nombre_clases, nombre_instructores = nombre_instructores, horario_clases = horario_clases, ubicacion_clases = ubicacion_clases)
    
    else:
        return redirect(url_for('login'))
    
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
    if logged_in_admin:
        form = RegisterForm(request.form)
        if request.method == 'POST' and form.validate():
            nombre = form.nombre.data
            direccion = form.direccion.data
            correo = form.correo.data
            csv = form.csv_tarjeta.data
            vencimiento = form.vencimiento_tarjeta.data
            no_tarjeta = form.no_tarjeta.data
            titular = form.titular_tarjeta.data

            if correo.find('@') != -1:
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
            else:
                error = "Asegurate de escribir un correo valido"
                return render_template('register_users.html', form=form, error= error)
            

        return render_template('register_users.html', form=form)    
    else:
        return redirect(url_for('login'))
    
#Borrar un usuario
class deleteForm(Form):
    correo = StringField('Ingresa el correo del usuario:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )

#Borrar a un usuario en especifico
@app.route('/delete_users', methods=['GET', 'POST'])
def delete_users():
    if logged_in_admin:
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
            #print(email_user)
            resultado_borrar = api.delete_user(email_user)
            if resultado_borrar == False:
                error = 'El correo que ingresaste no esta en la base de datos, vuelve a intentarlo'
                return render_template('delete_users.html', error = error, form = form, id_usuarios = id_usuarios, nombres_usuarios = nombres_usuarios, correos_usuarios = correos_usuarios, direcciones_usuarios = direcciones_usuarios)
            else:
                return redirect(url_for('home')) 
        return render_template('delete_users.html', form = form, id_usuarios = id_usuarios, nombres_usuarios = nombres_usuarios, correos_usuarios = correos_usuarios, direcciones_usuarios = direcciones_usuarios)
            
    else:
        return redirect(url_for('login'))
    
#Borrar una clase
class deleteClassForm(Form):
    id_clase = StringField('Ingresa el ID de la clase ha borrar:', [
        validators.DataRequired(),
        validators.Length(min=1, max=50)]
        )

#Borra una clase en especifico
@app.route('/delete_class', methods=['GET', 'POST'])
def delete_class():
    if logged_in_admin:
        form = claseForm(request.form)
        
        todas_clases = api.get_classes()
        nombre_todas_clases = []
        id_todas_clases = []
        nombre_todos_instructores = []
        horarios_todas_clases = []
        aux_nombre_instructores = []
        aux_horarios = []

        for i in range(len(todas_clases)):
            if int(todas_clases[i]['Cancelada']) == 0:
                nombre_todas_clases.append(todas_clases[i]['Nombre'])
                id_todas_clases.append(todas_clases[i]['_id'])
                for x in range(len(todas_clases[i]['Instructores'])):
                    
                    coach = api.get_one_instructor_id(todas_clases[i]['Instructores'][x])
                    nombre_coach = coach['Nombre_completo']
                    nombre_coach = ' ' + nombre_coach + ' (' + str(x) + ') '
                    aux_nombre_instructores.append(nombre_coach.encode('utf-8'))

                aux_nombre_instructores = ', '.join(map(str, aux_nombre_instructores))
                nombre_todos_instructores.append(aux_nombre_instructores)
                aux_nombre_instructores = []

                for p in range(len(todas_clases[i]['Horarios'])):
                    hors = todas_clases[i]['Horarios'][p]
                    hors = ' ' + hors + ' (' + str(p) + ') '
                    aux_horarios.append(hors.encode('utf-8'))
                aux_horarios = ', '.join(map(str, aux_horarios))
                horarios_todas_clases.append(aux_horarios)
                aux_horarios= []

        form = deleteClassForm(request.form)
        if request.method == 'POST' and form.validate():
            id_clase = form.id_clase.data
            
            clase_info = api.get_one_class(id_clase)

            if clase_info is not False: #Existe la clase ha borrar
                if clase_info['Cancelada'] == 0:
                    resultado_borrar = api.delete_class(id_clase)
                    print(resultado_borrar)
                    return redirect(url_for('home'))
                else:
                    error = 'Clase ya cancelada, inserta un id de las clases que aparecen en la lista'
                    return render_template('delete_class.html', form=form, error = error, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)

            else:
                error = 'No existe la clase con el id dado, checa bien la tabla'
                return render_template('delete_class.html', form=form, error = error, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)

        return render_template('delete_class.html', form = form, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)
    
    else:
        return redirect(url_for('login'))

    

#Form para la dieta al crearla
class instructorForm(Form):
    nombre_instructor = StringField('Nombre del instructor:', [
        validators.DataRequired(),
        validators.Length(min=3, max=500)]
        )
    direccion_instructor = StringField('Direccion del instructor:', [
        validators.DataRequired(),
        validators.Length(min=3, max=500)]
        )
    email_instructor =  StringField('Correo del instructor:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirmar_contrasenia', message='No coincide las contrasenias')
    ])
    confirmar_contrasenia = PasswordField('Confirmar password')



#Crear un instructor
@app.route('/register_instructors', methods=['GET', 'POST'])
def register_instructors():
    if logged_in_admin:
        form = instructorForm(request.form)
        #print(api.get_all_instructors())
        if request.method == 'POST' and form.validate():
            nombre_instructor = form.nombre_instructor.data
            direccion_instructor = form.direccion_instructor.data
            email_instructor = form.email_instructor.data

            password = sha256_crypt.encrypt(str(form.password.data))

            #signup_mongo = api.create_instructor(nombre_instructor, direccion_instructor, email_instructor)
            
            if email_instructor.find('@') != -1:
                domain = email_instructor.rsplit('@', 1)[1]

                #GUARDAR EN LA BASE DE DATOS LOS DATOS INGRESADOS
                if domain == 'mambafit.com': #para que sea un instructor autentico por el dominio
                    signup_redis = api.create_session(email_instructor, password)
                    if signup_redis == True:
                        session['register'] = True
                        signup_mongo = api.create_instructor(nombre_instructor, direccion_instructor, email_instructor)
                        return redirect(url_for('home'))
                    else:
                        error = "El correo que ingresaste se encuentra asociado a una cuenta"
                        return render_template('register_instructors.html', form=form, error= error)
                else:
                    error = "El correo debe ser de dominio mamba"
                    return render_template('register_instructors.html', form=form, error= error)
            else:
                error = "Asegurate de escribir un correo valido"
                return render_template('register_instructors.html', form=form, error= error)
            
        return render_template('register_instructors.html', form = form)
    
    else:
        return redirect(url_for('login'))
    

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
    if logged_in_instructor:
        form = dietaForm(request.form)
        if request.method == 'POST' and form.validate():
            nombre_comida = form.nombre_comida.data
            ingredientes = form.ingredientes.data
            descripcion = form.descripcion.data
            correo_cliente = form.correo_cliente.data

            if correo_cliente.find('@') != -1:
                domain = correo_cliente.rsplit('@', 1)[1]

                if domain != "mambafit.com": #para el administrador
                    signup_redis = api.get_password_user(correo_cliente)
                    if signup_redis:
                        dieta = api.crear_dieta(nombre_comida, ingredientes, descripcion, correo_cliente)
                        return redirect(url_for('home'))
                    else:
                        error = "No existe correo que ingresaste"
                        return render_template('crear_dieta.html', form=form, error= error)
                else:
                    error = "La dieta es para los clientes, no para los instructores"
                    return render_template('crear_dieta.html', form=form, error= error)
            else:
                error = "Asegurate de escribir un correo valido"
                return render_template('crear_dieta.html', form=form, error= error)
            
        return render_template('crear_dieta.html', form = form)    
    else:
        return redirect(url_for('login'))
    

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
    horarios =  StringField('Horarios Clase:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )
    ubicacion =  StringField('Ubicacion Clase:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )

#Crear una clase desde el instructor
@app.route('/crear_clase', methods=['GET', 'POST'])
def crear_clase():
    if logged_in_instructor:
        #print(api.get_classes())
        form = claseForm(request.form)
        
        todas_clases = api.get_classes()
        nombre_todas_clases = []
        id_todas_clases = []
        nombre_todos_instructores = []
        horarios_todas_clases = []
        aux_nombre_instructores = []
        aux_horarios = []

        for i in range(len(todas_clases)):
            if int(todas_clases[i]['Cancelada']) == 0:
                nombre_todas_clases.append(todas_clases[i]['Nombre'])
                id_todas_clases.append(todas_clases[i]['_id'])
                '''for x in range(len(todas_clases[i]['Instructores'])):
                    nombre_todos_instructores.append(todas_clases[i]['Instructores'][x])
                for p in range(len(todas_clases[i]['Horarios'])):
                    horarios_todas_clases.append(todas_clases[i]['Horarios'][p])'''
                #nombre_todos_instructores.append(todas_clases[i]['Instructores'])
                for x in range(len(todas_clases[i]['Instructores'])):
                    
                    coach = api.get_one_instructor_id(todas_clases[i]['Instructores'][x])
                    nombre_coach = coach['Nombre_completo']
                    nombre_coach = ' ' + nombre_coach + ' (' + str(x) + ') '
                    aux_nombre_instructores.append(nombre_coach.encode('utf-8'))

                aux_nombre_instructores = ', '.join(map(str, aux_nombre_instructores))
                nombre_todos_instructores.append(aux_nombre_instructores)
                aux_nombre_instructores = []

                for p in range(len(todas_clases[i]['Horarios'])):
                    hors = todas_clases[i]['Horarios'][p]
                    hors = ' ' + hors + ' (' + str(p) + ') '
                    aux_horarios.append(hors.encode('utf-8'))
                aux_horarios = ', '.join(map(str, aux_horarios))
                horarios_todas_clases.append(aux_horarios)
                aux_horarios= []

        id_clase_propuesta = len(todas_clases) + 1

        #print(nombre_todos_instructores)

        if request.method == 'POST' and form.validate():
            nombre_clase = form.nombre_clase.data
            #CAMBIAR PARA QUE SE GENERE INCREMENTAL EL ID_CLASE
            id_clase = form.id_clase.data
            horarios = form.horarios.data
            ubicacion = form.ubicacion.data
            instructor = api.get_one_instructor_email(correo_usuario)
            id_instructor = instructor['ID_Instructor']
            instructor_inscrito = False

            clase_ya_creada = api.get_one_class(id_clase)
            if clase_ya_creada is False:
                #Crear clase o aniadir el instructor a ella
                id_clase_final = str(id_clase_propuesta)
                clase = api.create_class(nombre_clase, id_clase_final, id_instructor, horarios, ubicacion)
                return redirect(url_for('home'))
            else: #Clase ya esta creada
                if int(clase_ya_creada['Cancelada']) == 0: #Si no esta cancelada
                    msg = "Ya esta creada la clase, por lo que haz ingresado en ella como instructor"
                    for i in range(len(clase_ya_creada['Instructores'])):
                        if clase_ya_creada['Instructores'][i] == id_instructor:
                            instructor_inscrito = True
                    if instructor_inscrito is not True: #Si no esta el instructor
                        clase = api.insert_class_instructor_schedule(id_clase, id_instructor, horarios)
                    else:
                        clase = api.insert_class_schedule(id_clase, horarios)
                    return redirect(url_for('home'))
                else:
                    error = 'ID clase no disponible, intenta con otro ID'
                    return render_template('crear_clase.html', form=form, id_clase_propuesta = id_clase_propuesta, error = error, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)


        return render_template('crear_clase.html', form = form, id_clase_propuesta = id_clase_propuesta, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)
    
    else:
        return redirect(url_for('login'))
    

#Form para aniadir a un usuario a una clase
class claseUsuarioForm(Form):
    id_horario = StringField('ID del horario:', [
        validators.DataRequired(),
        validators.Length(min=1, max=50)]
        )
    id_clase = StringField('ID de la clase:', [
        validators.DataRequired(),
        validators.Length(min=1, max=500)]
        )
    id_instructor = StringField('ID del instructor:', [
        validators.DataRequired(),
        validators.Length(min=1, max=500)]
        )
    correo_usuario_c =  StringField('Correo del usuario a inscribir:', [
        validators.DataRequired(),
        validators.Length(min=3, max=50)]
        )

#Aniade a un usuario a una clase el instructor
@app.route('/add_user_to_class', methods=['GET', 'POST'])
def add_user_to_class():
    if logged_in_instructor:
        #print(api.get_classes())
        form = claseUsuarioForm(request.form)
        
        todas_clases = api.get_classes()
        nombre_todas_clases = []
        id_todas_clases = []
        nombre_todos_instructores = []
        horarios_todas_clases = []
        aux_nombre_instructores = []
        aux_horarios = [] 


        for i in range(len(todas_clases)):
            if int(todas_clases[i]['Cancelada']) == 0:
                nombre_todas_clases.append(todas_clases[i]['Nombre'])
                id_todas_clases.append(todas_clases[i]['_id'])
                '''for x in range(len(todas_clases[i]['Instructores'])):
                    nombre_todos_instructores.append(todas_clases[i]['Instructores'][x])
                for p in range(len(todas_clases[i]['Horarios'])):
                    horarios_todas_clases.append(todas_clases[i]['Horarios'][p])'''
                #nombre_todos_instructores.append(todas_clases[i]['Instructores'])
                for x in range(len(todas_clases[i]['Instructores'])):
                    coach = api.get_one_instructor_id(todas_clases[i]['Instructores'][x])
                    nombre_coach = coach['Nombre_completo']
                    correo_coach = coach['email']
                    nombre_coach = ' ' + nombre_coach + ' ( ID: ' + str(x) + ' ) '
                    #print(nombre_coach)
                    aux_nombre_instructores.append(nombre_coach)
                #[x.encode('utf-8') for x in aux_nombre_instructores]
                #print(aux_nombre_instructores)
                #aux_nombre_instructores = [r.encode('utf-8') for r in aux_nombre_instructores]
                aux_nombre_instructores = ', '.join(map(str, aux_nombre_instructores))
                nombre_todos_instructores.append(aux_nombre_instructores)
                #print(nombre_todos_instructores)
                aux_nombre_instructores = []
                for p in range(len(todas_clases[i]['Horarios'])):
                    hors = todas_clases[i]['Horarios'][p]
                    hors = ' ' + hors + ' (' + str(p) + ') '
                    aux_horarios.append(hors)
                aux_horarios = ', '.join(map(str, aux_horarios))
                horarios_todas_clases.append(aux_horarios)
                aux_horarios= []

        if request.method == 'POST' and form.validate():
            #CAMBIAR PARA QUE SE GENERE INCREMENTAL EL ID_CLASE
            id_clase = form.id_clase.data
            id_instructor = form.id_instructor.data
            id_horario = form.id_horario.data
            correo_usuario_c = form.correo_usuario_c.data
            
            existe_instructor = False
            existe_horario = False

            if id_instructor.isdigit() and id_clase.isdigit() and id_horario.isdigit():

                #checando si hay el instructor y el horario en la clase
                checar_clase = api.get_one_class(id_clase)
                if checar_clase is not False: #Si existe la contrasenia
                    if len(checar_clase['Instructores']) > int(id_instructor):
                        existe_instructor = True
                    if len(checar_clase['Horarios']) > int(id_horario):
                        existe_horario = True

                    if existe_instructor and existe_horario and id_clase in id_todas_clases: #Si hay clase, instructor y horario en la clase
                        existe_usuario = api.get_user(correo_usuario_c)
                        if existe_usuario is not None: #Si existe el usuario 
                            msg = "Agregado exitosamente"
                            print(existe_usuario['Clases'][0]['Horario'])
                            if existe_usuario['Clases'][0]['Horario'] == -1: #Si es su primera clase

                                modify_class_user = api.add_user_class(id_clase, id_instructor, id_horario, correo_usuario_c)
                                print(modify_class_user)
                                print("MODIFICADA")
                                print(api.get_user(correo_usuario_c))
                                return render_template('add_user_to_class.html', form=form, msg = msg, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)
                            else: #Si ya tiene clases, agrega la nueva
                                print(correo_usuario_c)
                                add_class_user = api.update_user_class(id_clase, id_instructor, id_horario, correo_usuario_c)
                                print(add_class_user)
                                print("AGREGADO")
                                print(api.get_user(correo_usuario_c))
                                return render_template('add_user_to_class.html', form=form, msg = msg, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)
                        else:
                            error = 'No existe el usuario asociado al correo dado'
                            return render_template('add_user_to_class.html', form=form, error = error, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)
                    else:
                        error = 'No existe la clase con los argumentos dados, escribelo de manera correcta de acuerdo a la lista'
                        return render_template('add_user_to_class.html', form=form, error = error, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)
                else:
                    error = 'No existe la clase con el id dado, escribelo de manera correcta de acuerdo a la lista'
                    return render_template('add_user_to_class.html', form=form, error = error, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)
            else:
                error = 'Escribe solo numeros en los ID`s'
                return render_template('add_user_to_class.html', form=form, error = error, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)


        return render_template('add_user_to_class.html', form = form, nombre_todas_clases = nombre_todas_clases, horarios_todas_clases = horarios_todas_clases, nombre_todos_instructores = nombre_todos_instructores, id_todas_clases = id_todas_clases)
    
    else:
        return redirect(url_for('login'))
    


if __name__ == "__main__":
    app.secret_key='12345'
    app.run(debug=True)