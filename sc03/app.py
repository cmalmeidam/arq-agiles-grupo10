from sc03 import create_app
from flask_restful import Api
from flask import Flask, Request
from .vistas import *

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaRespuesta, '/respuesta')


