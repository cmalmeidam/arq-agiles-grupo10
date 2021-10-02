from flask_restful import Resource
from flask import request
import jwt
import datetime

class VistaValidacion(Resource):

    def post(self):
        key = "secret"
        user = request.json["user"]
        token = request.json["token"]
        microservice = request.json["microservice"]

        try:
            decode = jwt.decode(token, key, algorithms="HS256")
        except jwt.InvalidSignatureError:
            msg = 'Token con firma inválida'
            code = 401
        except jwt.DecodeError:
            msg = 'Token con error en decodificación'
            code = 401
            
        return msg, code