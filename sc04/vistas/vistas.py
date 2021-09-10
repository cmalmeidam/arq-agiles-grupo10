from flask_restful import Resource
import random

class VistaRespuesta(Resource):

    def get(self):
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

        return respuesta, cod