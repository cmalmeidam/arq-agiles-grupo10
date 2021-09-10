from sc03 import create_app
from flask_restful import Resource, Api
from flask import Flask, request
import requests


app = create_app('default')
app_context = app.app_context()
app_context.push()