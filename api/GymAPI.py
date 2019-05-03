from flask import request, url_for, jsonify
from flask_api import FlaskAPI, status, exceptions
from DBmodels import Accounts
from datetime import datetime
from DBmodels import Gimnasio
from bson import ObjectId


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

        # Se adicionó para poder manejar ObjectID
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
