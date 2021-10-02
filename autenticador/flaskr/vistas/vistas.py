from flask_restful import Resource
import requests
from flask import request, jsonify
import logger
import jwt
import datetime
from ..modelos import db, Usuario
from random import randrange

def json_status(status_code, message):
    res = jsonify({
        'isBase64Encoded': False,
        'statusCode': status_code,
        'body': message
    })
    res.status = '%s %s' % (status_code, message)
    res.message = message
    return res

class Autenticar(Resource):

    def post (self):
        id1 = randrange(99999)
        id2 = randrange(99999)
        key = "secret";
        logger.logger.info('Ingresar Autenticar')
        logger.logger.info('Validacion usuario tenga corecta las credenciales')
        usuario = Usuario.query.filter(Usuario.nombre == request.json["usuario"],
                                       Usuario.contrasena == request.json["contrasena"]).first()
        db.session.commit()
        if usuario is None:
            requests.get('https://sqs.us-east-2.amazonaws.com/867579940304/alertas-monitor.fifo?Action=SendMessage',
                         params={'MessageBody': 'Autenticar ;' + 'UsuariocredencialesInvalidas ; ' + request.json["usuario"] + ' ; ' + request.json["ip"], 'MessageDeduplicationId': id1, 'MessageGroupId': id2})
            return "Credenciales invalidas", 404
        else:
            token_de_acceso = jwt.encode(
                {"exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=10), "usuario": request.json["usuario"],
                 "ip": request.json["ip"]}, key, algorithm="HS256");
            decode = jwt.decode(token_de_acceso, key, algorithms="HS256")
            logger.logger.info('decode = ' + str(decode))
            requests.get('https://sqs.us-east-2.amazonaws.com/867579940304/alertas-monitor.fifo?Action=SendMessage',
                         params={'MessageBody': 'Autenticar ;' + 'UsuariocredencialesValidas ; ' + request.json["usuario"] + ' ; ' + request.json["ip"],
                                 'MessageDeduplicationId': id1, 'MessageGroupId': id2})
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}


