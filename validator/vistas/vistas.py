from flask_restful import Resource

class VistaValidacion(Resource):

    def get(self):
        return 'Respuesta correcta', 200