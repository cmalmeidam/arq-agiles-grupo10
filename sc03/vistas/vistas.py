from flask_restful import Resource
import time, random
import logging

class VistaRespuesta(Resource):

    def get(self):
        logging.basicConfig(filename='./log/sc03.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
        t=random.randint(0, 300)
        timeResponse = str(t)
        while t:
            time.sleep(1)
            t -= 1

        logging.info("El microservicio SC03 respondio de forma correcta en " + timeResponse +" segundos")
        return "Respuesta correcta", 200