from pymongo import MongoClient
from bson import ObjectId
from api import config

class Gimnasio(object):

    def __init__(self):
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        self.collection = db.clientes


    def find(self):
        """
        Obtener todos los usuarios
        """
        cursor = self.collection.find()

        usuarios = []

        for usuario in cursor:
            # Se adiciono para poder manejar ObjectID
            usuario['_id'] = str(usuario['_id']) 
            usuarios.append(usuario)

        return usuarios

    def findOne(self, mail):
        """
        Obtener un usuario dado un correo
        """
        usuario = self.collection.find_one({'email': mail})
        # Se adiciono para poder manejar ObjectID
        if usuario is not None:
            usuario['email'] = str(usuario['email'])
            

        return usuario

    def createUser(self, user):
        """
        Crear un nuevo usuario
        """
        result = self.collection.insert_one(user)

        return result

    def deleteUser(self, email):
        """
        Eliminar un usuario
        """
        result = self.collection.delete_one({'email': email})

        if result.deleted_count == 1:
            return True
        else:  
            return False


    def updateUser(self, email, new_data):
        """
        Actualizar un ususario
        """
        result = self.collection.update_one({'email': email}, {"$set": new_data})

        if result.matched_count == 1:
            return True
        else:  
            return False

#CLASES
    def findClasses(self):
        """
        Obtener todas las clases
        """
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.clases
        
        clases = collection.find()
        all_classes = []

        for clase in clases:
            # Se adiciono para poder manejar ObjectID
            clase['_id'] = str(clase['_id']) 
            all_classes.append(clase)

        return all_classes

    def findOneClass(self, id):
        """
        Obtener una clase  dado su id
        """
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.clases
        
        clase = collection.find_one({'_id': id})
        if clase is not None:
            return clase
        else:
            return False

    def createClass(self, clase):
        """
        Crear una clase nueva
        """
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.clases
        
        clase = collection.insert_one(clase)

        return clase

    def insertClassInstructorSchedule(self, id_clase, id_instructor, horarios):
        """
        Insertar en una clase existente al instructor y el horario del mismo
        """
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.clases

        result = collection.update({'_id':id_clase}, {'$push': {'Instructores': id_instructor}})
        result = collection.update({'_id':id_clase}, {'$push': {'Horarios': horarios}})

        return result

    def insertClassSchedule(self, id_clase, horarios):
        """
        Insertar en una clase existente el horario del instructor
        """
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.clases

        result = collection.update({'_id':id_clase}, {'$push': {'Horarios': horarios}})

        return result


#DIETAS
    def findFood(self):
        '''
        Obtener todas las comidas
        '''
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.dietas
        
        cursor = collection.find()

        dietas = []

        for dieta in cursor:
            # Se adiciono para poder manejar ObjectID
            dieta['_id'] = str(dieta['_id']) 
            dietas.append(dieta)

        return dietas

    #obtener dietas de un usuario
    def findFoodUser(self, email):
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.dietas
        
        #cursor = collection.replace_one({'Id_Cliente': 'U000001'}, {'Id_comida': 0, 'Nombre_comida': 'Pollo ahumado', 'Id_Cliente': 'act@gmail.com', 'Ingredientes': '100 gr pollo, 100 gr de brocoli, 100 gr papa', 'Descripcion': 'Preparala sin aceite y cocinala lentamente al fuego, el brocoli cocinalo al vapor, y la papa al horno'})

        cursor = collection.find({'Id_Cliente': email})
    
        dietas = []
        
        for dieta in cursor:
            # Se adiciono para poder manejar ObjectID
            dieta['_id'] = str(dieta['_id']) 
            dietas.append(dieta)
        
        return dietas

    def createFood(self, diet):
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.dietas

        cursor = collection.insert_one(diet)

        print(cursor)
        print(cursor.inserted_id)
        if cursor.inserted_id is not None:
            return True
        else:
            return False


#INSTRUCTORES
    def findInstructors(self):
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.instructores
        
        #cursor = collection.replace_one({'Id_Cliente': 'U000001'}, {'Id_comida': 0, 'Nombre_comida': 'Pollo ahumado', 'Id_Cliente': 'act@gmail.com', 'Ingredientes': '100 gr pollo, 100 gr de brocoli, 100 gr papa', 'Descripcion': 'Preparala sin aceite y cocinala lentamente al fuego, el brocoli cocinalo al vapor, y la papa al horno'})

        cursor = collection.find()
    
        instructores = []
        
        for instructor in cursor:
            # Se adiciono para poder manejar ObjectID
            instructor['_id'] = str(instructor['_id']) 
            instructores.append(instructor)
        
        return instructores

    def findOneInstructor(self, email):
        client = MongoClient(config.MONGO_URI)
        db = client.gimnasio
        collection = db.instructores
        
        cursor = collection.find_one({'ID_Instructor': email})
        
        return cursor