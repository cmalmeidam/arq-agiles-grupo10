import json
from random import randrange
from flask_restful import Resource
from flask import request
import jwt
import logging
import requests

class VistaValidacion(Resource):

    def post(self):
        id1 = randrange(99999)
        id2 = randrange(99999)
        logging.basicConfig(filename='./log/validator.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding = "UTF-8")
        key = "secret"
        user = request.json["user"]
        token = request.json["token"]
        microservice = request.json["microservice"]

        try:
            decode = jwt.decode(token, key, algorithms="HS256")
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

        except jwt.InvalidSignatureError:
            msg = 'Token con firma inválida'
            code = 401
        except jwt.DecodeError:
            msg = 'Token con error en decodificación'
            code = 401
        except jwt.ExpiredSignatureError:
            msg = 'Token expirado'
            code = 419
        
        logging.info("El microservicio Validator respondio: " + msg)
        requests.get('https://sqs.us-east-2.amazonaws.com/867579940304/alertas-monitor.fifo?Action=SendMessage',
                        params={'MessageBody': 'Validador ;' + 'respondio el usuario ; ' + user + ' ; ' + msg + ' ; ' + code, 'MessageDeduplicationId': id1, 'MessageGroupId': id2})
        return msg, code