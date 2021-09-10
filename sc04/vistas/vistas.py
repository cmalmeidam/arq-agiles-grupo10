from flask_restful import Resource
import random, logging

class VistaRespuesta(Resource):

    def get(self):
        logging.basicConfig(filename='./log/sc04.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', encoding = "UTF-8")
        option=random.randint(0, 4)
        if option == 0:
            respuesta = "Repuesta correcta"
            cod = 200
        elif option == 1:
            respuesta = "Repuesta incorrecta"
            cod = 200
        elif option == 2:
            respuesta = "Repuesta con incoherencias"
            cod = 300
        elif option == 3:
            respuesta = "El servidor no procesará la solicitud"
            cod = 400
        elif option == 4:
            respuesta = "Error interno en el servidor"
            cod = 500
        logging.info("El microservicio SC04 respondio: " + respuesta +", "+ str(cod)+ " en " + str(1) +" s")
        return respuesta, cod