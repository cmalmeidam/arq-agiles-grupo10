from flask import Flask
from flask import jsonify
import logging
from flask import request
from requests_futures.sessions import FuturesSession

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

logging.basicConfig(filename='comandos.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


@app.route("/", methods=["GET"])

def protected():
    user = request.json["user"]
    token = request.json["token"]
    session = FuturesSession()
    validacion = session.post('http://127.0.0.1:5000/',json={"user": user, "token": token, "microservice": "query"})
    if (validacion.result().status_code != 200):
        return "Petición no válida", 403
    else:
        return "Petición válida", 200

if __name__ == "__main__":
    app.run()