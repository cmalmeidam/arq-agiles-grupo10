from validator import create_app
from flask_restful import Resource, Api
from flask import Flask, Request
from flask_jwt_extended import JWTManager
from .vistas import *

app = create_app('default')
app_context = app.app_context()
app_context.push()

api = Api(app)
api.add_resource(VistaValidacion, '/validacion')

jwt = JWTManager(app)
