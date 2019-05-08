from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from api.DBmodels import Accounts, Gimnasio
from datetime import datetime
from bson import ObjectId
import json
import random

class GymAPI(object):

#USUARIOS
    #Obtener todos los usuarios
    def get_all_users(self):
        mongodb = Gimnasio.Gimnasio()
        users = mongodb.find()
        return users

    #Obtener un solo usuario dado un correo
    def get_user(self, email):
        mongodb = Gimnasio.Gimnasio()
        user = mongodb.findOne(email)
        return user

    #Obtener nombre de usuario dado un correo
    def get_name_user(self, email):
        user = self.get_user(email)
        if user is None:
            return "Nombre No encontrado"
        else:
            return user['Nombre_completo']

    #Obtener el numero de usuarios que hay en la base de datos de mongodb
    def get_number_of_users(self):
        mongodb = Gimnasio.Gimnasio()
        no_users = mongodb.getNumberOfUsers()
        return no_users

    def update_user(self):
        mongodb = Gimnasio.Gimnasio()
        p = {}
        no_users = mongodb.updateUser('s',p)

   #Actualizar los datos de sus clases del usuario 
    def update_user_class(self, id_clase, id_instructor, id_horario, correo_usuario):
        mongodb = Gimnasio.Gimnasio()
        new_class = {
            'Horario': int(id_horario), 
		    'Instructor': int(id_instructor), 
			'Id_clase': str(id_clase)
        }
        clases_usuario_actualizadas = mongodb.updateUserClass(new_class, correo_usuario)

        return clases_usuario_actualizadas

    #Aniade clases al usuario 
    def add_user_class(self, id_clase, id_instructor, id_horario, correo_usuario):
        mongodb = Gimnasio.Gimnasio()
        new_class = {
            'Horario': int(id_horario), 
		    'Instructor': int(id_instructor), 
			'Id_clase': str(id_clase)
        }
        clases_usuario_actualizadas = mongodb.addUserClass(new_class, correo_usuario)

        return clases_usuario_actualizadas


#CLASES
    #Obtener todas las clases
    def get_classes(self):
        mongodb = Gimnasio.Gimnasio()
        classes = mongodb.findClasses() #CAMBIAR
        return classes

    #Obtener clases de un usuario
    def get_classes_user(self, email):
        user = self.get_user(email)
        if user is None:
            return None
        else:
            classes_user = user['Clases']
            '''print(cl)
            classes_user = []
            for clase in user['Clases']:
                classes_user.append(clase['Horario'])
                classes_user.append(clase['Instructor'])
                classes_user.append(int(clase['Id_clase'])) #CHECAAAAARRRRRR
            print(classes_user)'''
            return classes_user
        #return cl

    #Obtener una clase dado el id
    def get_one_class(self, id):
        mongodb = Gimnasio.Gimnasio()
        clase = mongodb.findOneClass(id)
        return clase

    #Insertar una nueva clase
    def create_class(self, nombre_clase, id_clase, instructores, horarios, ubicacion):
        mongodb = Gimnasio.Gimnasio()
        class_data = {
            'Nombre' : nombre_clase,
            '_id' : id_clase,
            'Instructores':
                [
                    instructores
                ], 
            'Horarios':
                [
                    horarios
                ],
            'Ubicacion': ubicacion,
            'Cancelada':0
        }
        result = mongodb.createClass(class_data)
        return result

    #Insertar en una clase existente al instructor y el horario del mismo
    def insert_class_instructor_schedule(self, id_clase, id_instructor, horarios):
        mongodb = Gimnasio.Gimnasio()
        result = mongodb.insertClassInstructorSchedule(id_clase, id_instructor, horarios)
        return result

    def insert_class_schedule(self, id_clase, horarios):
        mongodb = Gimnasio.Gimnasio()
        result = mongodb.insertClassSchedule(id_clase, horarios)
        return result

    def delete_class(self, id_clase):
        mongodb = Gimnasio.Gimnasio()
        result = mongodb.deleteClass(id_clase)
        return result


#SESIONES REDIS
    #Para comparar hashes y dejar o no pasar
    def get_password_user(self, email):
        redis = Accounts.Sessions()
        password = redis.getUserPassword(email)
        return password
    
    #Para crear un usuario en redis
    def create_session(self, email, password):
        redis = Accounts.Sessions()
        signup_redis = redis.signUp(email, password)

        return signup_redis
        #MONGO TAMBIEN

    def create_user(self, nombre, direccion, correo, tarjeta, titular, csv, vencimiento):
        #id_generado = random.randint(100000, 999999)
        #id_usuario = 'U' + str(id_generado)

        print("Size of mongodb")
        id_i = self.get_number_of_users() + 1
        final_id = 'U' +  str(id_i).zfill(6)
        print(final_id)
        id_usuario = final_id
        print("END")

        mongodb = Gimnasio.Gimnasio()
        user_data = {
            'Nombre_completo' : nombre,
            'Direccion' : direccion,
            'email' : correo,
            'Tarjeta': 
                {
                'CSV': csv,
                'Vencimiento': vencimiento, 
                'No_tarjeta': tarjeta, 
                'Titular': titular
                }, 
            'ID': id_usuario, 
            'Clases':[
                {
                    'Horario': -1, 
                    'Instructor': -1, 
                    'Id_clase': '-1'
                }
                ]
        }
        #user_json = json.loads(user_data)
        print(user_data)

        data = {}
        data['key'] = 'value'
        json_data = json.dumps(data)
        print(json_data)

        result = mongodb.createUser(user_data)
    
    #Borrar un usuario
    def delete_user(self, correo):
        mongodb = Gimnasio.Gimnasio()
        result_mongo = mongodb.deleteUser(correo)
        redis = Accounts.Sessions()
        result_redis = redis.deleteOne(correo)
        return result_mongo
    
    #Actualizar un usuario
    def update_users(elf, nombre, direccion, correo, tarjeta, ID, clases):
        mongodb = Gimnasio.Gimnasio()
        user_data = {
            'Nombre_completo' : nombre,
            'Direccion' : direccion,
            'email' : correo,
            'Tarjeta': 
                {
                'CSV': '123',
                'Vencimiento': "datetime.datetime(2022, 2, 2, 6, 0)", 
                'No_tarjeta': '5406250000000021', 
                'Titular': nombre
                }, 
            'ID': 'U000002', 
            'Clases':[
                {
                    'Horario': 1, 
                    'Instructor': 0, 
                    'Id_clase': '0'
                }
                ]
        }
#COMIDA
    #Obtener todas las comidas
    def get_food(self):
        mongodb = Gimnasio.Gimnasio()

        result = mongodb.findFood()
        
        return result

    #Obtener comida de un usuario
    def get_food_user(self, email):
        mongodb = Gimnasio.Gimnasio()

        result = mongodb.findFoodUser(email)
        
        return result

    #Crear una comida para un usuario en especifico
    def crear_dieta(self, nombre_comida, ingredientes, descripcion, correo_cliente):
        mongodb = Gimnasio.Gimnasio()

        dieta = {
            'Id_comida' : 0,
            'Nombre_comida' : nombre_comida,
            'Id_Cliente': correo_cliente, 
            'Ingredientes' : ingredientes,
            'Descripcion': descripcion,
        }

        result = mongodb.createFood(dieta)
        
        return result


#INSTRUCTORES
    #Obtener todas las comidas
    def get_all_instructors(self):
        mongodb = Gimnasio.Gimnasio()

        result = mongodb.findInstructors()
        
        return result

    #Obtener un instructor en particular
    def get_one_instructor_id(self, id):
        mongodb = Gimnasio.Gimnasio()

        result = mongodb.findOneInstructorId(id)
        
        return result

    #Obtener un instructor en particular
    def get_one_instructor_email(self, email):
        mongodb = Gimnasio.Gimnasio()

        result = mongodb.findOneInstructorEmail(email)
        
        return result

    #Crear un instructor
    def create_instructor(self, nombre_instructor, direccion_instructor, email_instructor):
        #id_generado = random.randint(100000, 999999)
        #id_usuario = 'U' + str(id_generado)

        print("Size of mongodb instructors")
        id_i = self.get_number_of_instructors() + 1
        final_id = 'I' +  str(id_i).zfill(6)
        print(final_id)
        id_instructor = final_id

        mongodb = Gimnasio.Gimnasio()
        instructor_data = {
            'ID_Instructor' : id_instructor,
            'Nombre_completo' : nombre_instructor,
            'Direccion' : direccion_instructor,
            'email': email_instructor, 
            'Clases':[
                {
                    'Horario': '-1',
                    'Id_clase': -1
                }
                ]
        }
        #user_json = json.loads(instructor_data)
        print(instructor_data)

        result = mongodb.createInstructor(instructor_data) 
        return result#true or false

    #Crear un instructor
    def get_number_of_instructors(self):
        mongodb = Gimnasio.Gimnasio()
        no_instructors = mongodb.getNumberOfInstructors()
        return no_instructors

app = FlaskAPI(__name__)

@app.route('/LOGIN/<string:usr>/<string:pswd>/', methods=['GET'])
def login(usr, pswd):
    redis = Accounts.Sessions()
    dbsize = redis.Login(usr)

    if dbsize.decode("utf-8")==pswd:
        return "1"
        #return jsonify({"Sesiones activas: ": 1})
    else:
        return jsonify({"Sesiones activas: ": 0})

@app.route('/SIGNUP/<string:usr>/<string:pswd>/', methods=['GET'])
def signup(usr, pswd):
    redis = Accounts.Sessions()
    dbsize = redis.Signup(usr, pswd)

    if dbsize == "1":
        return "Success"
    else:
        return "Already signed"

@app.route("/", methods=['GET', 'POST'])
def list():
    redis = Accounts.Sessions()

    now = datetime.now()

    timestamp = datetime.timestamp(now)
    
    #redis.add(timestamp)

    mongodb = Gimnasio.Notes()

    if request.method == 'POST':
        note = request.data

        result = mongodb.create(note)

        # Se adiciono para poder manejar ObjectID
        note['_id'] = str(note['_id'])

        return note, status.HTTP_201_CREATED

    return mongodb.find()


@app.route("/n/", methods=['GET', 'PUT', 'DELETE'])
def notes_detail(key):

    mongodb = Gimnasio.Notes()

    if request.method == 'PUT':
        note = request.data
        mongodb.update(key, note)
        return note

    elif request.method == 'DELETE':
        mongodb.delete(key)
        return '', status.HTTP_204_NO_CONTENT

    # request.method == 'GET'
    note =  mongodb.findOne(key)
    if not note:
        raise exceptions.NotFound()
    else:
        return note

    return jsonify(key)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
