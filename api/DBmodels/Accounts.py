import redis
from api import config

class Sessions(object):

    def __init__(self):
        if config.REDIS_PASSWORD:
            self.instance = redis.StrictRedis(
                host=config.REDIS_HOST,
                port=config.REDIS_PORT,
                password=config.REDIS_PASSWORD)
        else:
            self.instance = redis.StrictRedis(
                host= config.REDIS_HOST,
                port=config.REDIS_PORT)


    def getUserPassword(self,user):
        """ Obtener un Password dado un correo """

        password = self.instance.get(user)

        if password is None: #Not found
            return False 
        else: 
            return password

    def signUp(self,user,password):
        """ Registra usuario y password """

        if self.instance.get(user) is None:
            signup = self.instance.set(user,password)
            return True 
        else: #Duplicado
            return False

    def add(self, id):
        """ Crea una nueva sesion en Redis """

        result = self.instance.set(id, 1)

        return result

    def deleteOne(self, email):
        ''' Borrar al eliminar un usuario'''

        result = self.instance.delete(email)

        return result