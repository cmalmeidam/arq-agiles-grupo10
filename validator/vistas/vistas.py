import json
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
        except jwt.ExpiredSignatureError:
            msg = 'Token expirado'
            code = 419
        
        ip = decode.get('ip')[0:10]

        if decode.get('usuario') == user :
            if decode.get('rol') == "admin":
                if ip == "186.84.21.":
                    msg = "Usuario autorizado"
                    code = 200
                else:
                    msg = "Posible suplantación de usuario"
                    code = 429
            elif decode.get('rol') == "consulta":
                if ip == "186.84.35.":
                    if microservice == "query":
                        msg = "Usuario autorizado"
                        code = 200
                    else:
                        msg = "El usuario no tiene permisos para está acción"
                        code = 403
                else:
                    msg = "Posible suplantación de usuario"
                    code = 429
            else:
                msg = "No tiene ningún rol asociado al usuario"
                code = 401
        else:
            msg = "Posible suplantación de usuario"
            code = 429
            
        return msg, code