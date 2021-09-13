import logging
from flask import Flask, request
from random import randrange

logging.basicConfig(filename='sc02.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__)

@app.route('/respuesta', methods=['GET'])
def respuesta():
    res = randrange(2)
    cod = 200
    if res==1:
        cod=500
    logging.info("El microservicio SC02 respondio: " +", "+ str(cod))
    return 'Omision', cod

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5003)