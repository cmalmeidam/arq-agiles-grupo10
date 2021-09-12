from flaskr import create_app
from flask_restful import Api
from flask_cors import CORS, cross_origin
from .vistas import PublicarMsj
from .vistas import PublicarMsj2

app = create_app('default')
app_context = app.app_context()
app_context.push()

cors = CORS(app)
api = Api(app)
api.add_resource(PublicarMsj, '/publicar')
api.add_resource(PublicarMsj2, '/publicar2')
