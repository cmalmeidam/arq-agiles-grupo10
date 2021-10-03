import time, random, string
from generadorEscenarios import create_app
from concurrent.futures import as_completed, ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from requests.exceptions import ConnectTimeout, HTTPError, ReadTimeout
from pprint import pprint
import requests
from flask import jsonify
import uuid
import logging

app = create_app('default')
app_context = app.app_context()
app_context.push()
logging.basicConfig(filename='./log/escenarios.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding = "UTF-8")

# validUsers in db or service
users = [{ "email": "chalmeida", "password": "chalmeida"},{ "email": "user1", "password": "user1"}]

# add urls of services to be monitored, states are not considered yet in the logic
currentServices = [{"url": 'http://localhost:5003', "nombre": "consulta"},{"url": 'http://localhost:5002', "nombre": "comando"}]
currentServicesLength = len(currentServices)

# Authentication Service
authService = { "url": 'http://localhost:5000/autenticar', "nombre": "authenticacion"}

def response_hook(resp, *args, **kwargs):
    print(resp)
    # parse the json storing the result on the response object
    resp.data = resp.json()


def json_status(status_code, message):
    res = jsonify({
        'isBase64Encoded': False,
        'statusCode': status_code,
        'body': message
    })
    res.status = '%s %s' % (status_code, message)
    res.message = message
    return res


def post(parameters):
    r = requests.get('https://sqs.us-east-2.amazonaws.com/867579940304/alertas-monitor.fifo?Action=SendMessage',
                     params=parameters)
    return json_status(200, 'Message sent')


def format_prepped_request(prepped, encoding=None):
    # prepped has .method, .path_url, .headers and .body attribute to view the request
    encoding = encoding or requests.utils.get_encoding_from_headers(prepped.headers)
    body = prepped.body.decode(encoding) if encoding else '<binary data>'
    headers = '\n'.join(['{}: {}'.format(*hv) for hv in prepped.headers.items()])
    return f"""\
{prepped.method} {prepped.path_url} HTTP/1.1
{headers}

{body}"""

## Caso 1 Credenciales Incorrectas
def credencialesIncorrectas(session):
    session = FuturesSession()
    authResponse = session.post(authService['url'],json={"usuario": "chalmeida", "contrasena": "fakePassword", "ip":"186.84.21.99" })
    print (authResponse.result().json())

## Caso 2 Credenciales Correctas

def credencialesCorrectas(session):
    session = FuturesSession()
    authResponse = session.post(authService['url'],json={"usuario": "chalmeida", "contrasena": "chalmeida", "ip":"186.84.21.99" })
    print (authResponse.result().json())

## Caso 3 Token Válido

def tokenValido(session):
    session = FuturesSession()
    authResponse = session.post(authService['url'],json={"usuario": "chalmeida", "contrasena": "chalmeida", "ip":"186.84.21.99" })
    contentResponse = authResponse.result().json()
    return session.get(currentServices[0]['url'], json={"token": contentResponse["token"], "usuario": "chalmeida"})

## Caso 4 Token Inválido
def tokenInvalido(session):
    session = FuturesSession()
    authResponse = session.post(authService['url'],json={"usuario": "chalmeida", "contrasena": "chalmeida", "ip":"186.84.21.99" })
    authResponse.result().json()
    return session.get(currentServices[0]['url'], json={"usuario": "chalmeida", "token": ''.join(random.choices(string.ascii_letters + string.digits, k=32))})

## Caso 5 Token Suplantado

def tokenSuplantado(session):
    session = FuturesSession()
    authResponse = session.post(authService['url'],json={"usuario": "chalmeida", "contrasena": "chalmeida", "ip":"186.84.21.99" })
    contentResponse = authResponse.result().json()
    print(contentResponse)
    return session.get(currentServices[0]['url'], json={"usuario": "chalmeida", "token": contentResponse["token"]})

## Caso 6 Token Válido no Autorizado
def tokenNoAutorizado(session):
    session = FuturesSession()
    authResponse = session.post(authService['url'],json={"usuario": "usuario1", "contrasena": "usuario1", "ip":"186.84.35.15" })
    contentResponse = authResponse.result().json()
    print(contentResponse)
    return session.get(currentServices[1]['url'], json={"usuario": "usuario1", "token": contentResponse["token"]})

## Caso 7 Token Expirado
def tokenExpirado(session):
    session = FuturesSession()
    authResponse = session.post(authService['url'],json={"usuario": "usuario1", "contrasena": "usuario1", "ip":"186.84.35.15", "ttl": 1 })
    contentResponse = authResponse.result().json()
    print(contentResponse)
    time.sleep(10)
    return session.get(currentServices[0]['url'], json={"usuario": "usuario1", "token": contentResponse["token"]})

caseArray = [ credencialesIncorrectas, credencialesCorrectas, tokenInvalido, tokenInvalido, tokenSuplantado, tokenNoAutorizado ]
caseArrayLength = len(caseArray)

@app.route('/')
def get_data():
    countErrOmision = 0
    with FuturesSession(executor=ThreadPoolExecutor(max_workers=10)) as session:
        promises = []
        for i in range(10):
            """logic to assing randomly a service and attach info to the request to process event in case of error"""
            t = random.randint(1, caseArrayLength) - 1
            currentSession = caseArray[t](session)
            if (currentSession is None):
                print("Respuesta caso credenciales, no se realizará llamada a servicios")
                print("Caso " + str(t + 1))
                ## Logger caso 1 y 2
                logging.info("Request " + str(i + 1) + " se creó con caso " + str(t + 1))
            else:
                currentSession.requestDetails = {
                    "case": str(t + 1),
                    "request": str(i + 1)
                }
                promises.append(currentSession)
        print(promises)
        for promise in as_completed(promises):
            try:
                promise.result().content
                ''' Revisar logica de criterio para rechazar request HTTP '''
                #Esta podría ser una opción para simular un error de Conección generando una variable aleatoria o recibiendo alguna instrucción del servicio en el body o el status code
                if(promise.result().status_code != 200):
                    raise HTTPError()
                print("RespuestaCorrecta")
                print(promise.requestDetails)
                print(promise.result().status_code)
                logging.info("Request " + promise.requestDetails["request"] + " se creó con caso " + promise.requestDetails["case"])
            except HTTPError as e:
                '''Add logic for log in case theres an HTTP error response'''
                print("HTTPError")
                print(promise.requestDetails)
                logging.info("Request " + promise.requestDetails["request"] + " se creó con caso " + promise.requestDetails["case"])
    return 'Done'
