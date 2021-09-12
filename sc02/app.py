import logging
from flask import Flask, request

logging.basicConfig(filename='sc02.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def respuesta():
        logging.info('405')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)