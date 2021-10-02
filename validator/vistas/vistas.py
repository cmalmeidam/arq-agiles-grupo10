from flask_restful import Resource
from flask import request

class VistaValidacion(Resource):

    def post(self):
        user = request.json["user"]
        token = request.json["token"]
        microservice = request.json["microservice"]
        return 'Respuesta correcta es: ' + user, 200