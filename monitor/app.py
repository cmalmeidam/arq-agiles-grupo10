from monitor import create_app
from concurrent.futures import as_completed, ThreadPoolExecutor
from requests_futures.sessions import FuturesSession
from requests.exceptions import ConnectTimeout, HTTPError, ReadTimeout
from pprint import pprint
import requests


app = create_app('default')
app_context = app.app_context()
app_context.push()

def response_hook(resp, *args, **kwargs):
    print(resp)
    # parse the json storing the result on the response object
    resp.data = resp.json()

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
            currentSession = session.get('http://example.com',timeout=0.1)
            currentSession.requestType = i
            promises.append(currentSession)
        print(promises)
        for promise in as_completed(promises):
            try:
                return promise.result().content
            except ConnectTimeout as e:
                '''Add logic for log in case theres a timeout'''
                print(promise.requestType)
                print(format_prepped_request(e.request))
            except HTTPError as e:
                '''Add logic for log in case theres an HTTP error response'''
                print(e)
    return 'Test'