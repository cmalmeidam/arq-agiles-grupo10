from flask_restful import Resource

class VistaRespuesta(Resource):

    def get(self):
        return 'Respuesta correcta', 200