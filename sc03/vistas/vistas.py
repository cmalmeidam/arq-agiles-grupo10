from flask_restful import Resource
import time

class VistaRespuesta(Resource):

    def get(self):
        t=10
        while t:
            time.sleep(1)
            t -= 1

        return "Respuesta correcta", 200