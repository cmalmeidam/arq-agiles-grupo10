import logging
from flask import Flask, request

logging.basicConfig(filename='sc02.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def respuesta():
    if request.method == 'POST':
        request_data = 'Error en los datos'
        logging.info(request_data)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)