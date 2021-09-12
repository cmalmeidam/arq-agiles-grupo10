import time, random
from monitor import create_app
from concurrent.futures import as_completed, ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from requests.exceptions import ConnectTimeout, HTTPError, ReadTimeout
from pprint import pprint
import requests
import logger
from flask import jsonify
import uuid

app = create_app('default')
app_context = app.app_context()
app_context.push()

# add urls of services to be monitored, states are not considered yet in the logic
currentServices = [{"url": 'http://localhost:5000/respuesta', "nombre": "SCO3"},{"url": 'http://localhost:5001/respuesta', "nombre": "SCO4"}]
currentServicesLength = len(currentServices)


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
    logger.logger.info(r)
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


@app.route('/')
def get_data():
    with FuturesSession(executor=ThreadPoolExecutor(max_workers=10)) as session:
        promises = []
        for i in range(150):
            """logic to assing randomly a service and attach info to the request to process event in case of error"""
            t = random.randint(0, currentServicesLength) - 1
            currentSession = session.get(currentServices[t]["url"], timeout=2)
            currentSession.requestDetails = {
                "service": currentServices[t],
            }
            promises.append(currentSession)
        print(promises)
        for promise in as_completed(promises):
            try:
                time.sleep(1)
                promise.result().content
                print("RespuestaCorrecta")
                print(promise.requestDetails)
                msg = "El microservicio" + promise.requestDetails["service"]["nombre"] + "presenta" + "RespuestaCorrecta"
                post({'MessageBody': msg,
                      'MessageDeduplicationId': uuid.uuid4(), 'MessageGroupId': uuid.uuid4()})
            except ConnectTimeout as e:
                '''Add logic for log in case theres a timeout'''
                print("ConnectTimeout")
                print(promise.requestDetails)
                print(format_prepped_request(e.request))
                msg = "El microservicio" + promise.requestDetails["service"]["nombre"] + "tiene falla:" + "ConnectTimeout"
                post({'MessageBody': msg,
                      'MessageDeduplicationId': uuid.uuid4(), 'MessageGroupId': uuid.uuid4()})
            except HTTPError as e:
                '''Add logic for log in case theres an HTTP error response'''
                print("HTTPError")
                print(promise.requestDetails)
                msg = "El microservicio" + promise.requestDetails["service"]["nombre"] + "tiene falla:" + "HTTPError"
                post({'MessageBody': msg,
                      'MessageDeduplicationId': uuid.uuid4(), 'MessageGroupId': uuid.uuid4()})
            except requests.exceptions.ConnectionError as e:
                print("ConnectionError")
                print(promise.requestDetails)
                msg = "El microservicio" + promise.requestDetails["service"]["nombre"] + "tiene falla:" + "ConnectionError"
                post({'MessageBody': msg,
                      'MessageDeduplicationId': uuid.uuid4(), 'MessageGroupId': uuid.uuid4()})
            except requests.exceptions.ReadTimeout as e:
                print("ReadTimeoutError")
                print(promise.requestDetails)
                msg = "El microservicio" + promise.requestDetails["service"]["nombre"] + "tiene falla:" + "ReadTimeoutError"
                post({'MessageBody': msg,
                      'MessageDeduplicationId': uuid.uuid4(), 'MessageGroupId': uuid.uuid4()})
    return 'Test'
