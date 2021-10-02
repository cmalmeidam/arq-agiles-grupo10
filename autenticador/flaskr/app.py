from flaskr import create_app
from flask_restful import Api
from flask_cors import CORS, cross_origin
from .vistas import Autenticar
from flask_jwt_extended import JWTManager
from .modelos import db

app = create_app('default')
app_context = app.app_context()
app_context.push()
db.init_app(app)
db.create_all()

cors = CORS(app)
api = Api(app)


api.add_resource(Autenticar, '/autenticar')

jwt = JWTManager(app)
