from flask_restful import Resource
import time, random

class VistaRespuesta(Resource):

    def get(self):
        t=random.randint(0, 300)
        while t:
            time.sleep(1)
            t -= 1

        return "Respuesta correcta", 200