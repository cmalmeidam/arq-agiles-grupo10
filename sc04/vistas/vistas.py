from flask_restful import Resource
import random

class VistaRespuesta(Resource):

    def get(self):
        option=random.randint(0, 1)
        if option == 0:
            return "Respuesta correcta", 200
        elif option == 1:
            return "Respuesta incorrecta", 200