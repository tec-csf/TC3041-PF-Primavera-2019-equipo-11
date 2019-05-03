import redis
import config

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


    def Login(self,user):
        """ Valida usuario y password """

        size = self.instance.get(user)

        return size

    def Signup(self,user,password):
        """ Registra usuario y password """

        if self.instance.get(user) is None:
            size = self.instance.set(user,password)
            return "1"
        else:
            return "0"

    def add(self, id):
        """ Crea una nueva sesion en Redis """

        result = self.instance.set(id, 1)

        return result
