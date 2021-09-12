import logging
from flask import Flask, request

logging.basicConfig(filename='sc01.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__)

@app.route('/respuesta')
def respuesta():
        logging.info("corriendo")
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)