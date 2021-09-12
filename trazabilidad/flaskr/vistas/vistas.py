import boto3
from flask_restful import Resource
import requests
from flask import request, jsonify
import logger
from random import randrange
import os
import logging

def json_status(status_code, message):
    res = jsonify({
        'isBase64Encoded': False,
        'statusCode': status_code,
        'body': message
    })
    res.status = '%s %s' % (status_code, message)
    res.message = message
    return res

class PublicarMsj(Resource):
    def post (self):
        parametros = {'MessageBody': 'hola mundo 2', 'MessageDeduplicationId': 'prueba2', 'MessageGroupId': 'prueba2'}
        r = requests.get('https://sqs.us-east-2.amazonaws.com/867579940304/alertas-monitor.fifo?Action=SendMessage', params=parametros)
        logger.logger.info(r)
        return json_status(200, 'Message sent')

class Respuesta(Resource):
    logging.basicConfig(filename='trazabilidad.log', level=logging.INFO, format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', encoding="UTF-8")
    def get (self):
        dec = randrange(99999)
        cod = ''
        if dec % 2 == 0:
            cod = 200
        else:
            cod = 201

        logging.info("El microservicio SC04 respondio: " + "respuesta" +", "+ str(cod)+ " en " + str(1) +" s")
        return 'Servicio SC02', cod

class PublicarMsj2(Resource):
    def post (self):
        logger.logger.info('1. Ingresa a PublicarMsj2 ')
        try:
            sqs_client = boto3.client(
                'sqs',
                region_name=os.environ['AWS_REGION'],
                endpoint_url=os.environ['SQS_ENDPOINT'],
                use_ssl=os.environ['USE_SSL'] == '1',
                verify=False,
                aws_access_key_id=os.environ['ACCESS_KEY'],
                aws_secret_access_key=os.environ['SECRET_KEY'])
        except Exception as e:
            logger.logger.error(e)

        message = 'Prueba de servicios de colas'
        some_attribute = 'lo que sea'
        another_attribute = 'lo que sea 2'

        logger.logger.info('2. Set atributos ')

        try:
            id1 = randrange(99999)
            id2 = randrange(99999)
            queue_url = sqs_client.get_queue_url(QueueName=os.environ['SQS_QUEUE_NAME'])['QueueUrl']
            sqs_client.send_message(
                QueueUrl=queue_url,
                MessageGroupId=str(id1),
                MessageDeduplicationId=str(id2),
                MessageBody=message,
                MessageAttributes={
                    'some_attribute': {
                        'DataType': 'String',
                        'StringValue': some_attribute
                    },
                    'another_attribute': {
                        'DataType': 'String',
                        'StringValue': another_attribute
                    }
                }
            )
            logger.logger.info('Message sent')
            return json_status(200, 'Message sent')
        except Exception as e:
            logger.logger.error(e)
            return json_status(500, str(e))