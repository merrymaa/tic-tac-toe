from flask import Flask
from flask_jwt_extended import JWTManager
from web.route.game_routes import game_bp
from web.route.auth_routes import auth_bp
from  flask_reqcheck  import  ReqCheck

from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from flask_reqcheck import validate_body, get_valid_request, validate


def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "key"
    jwt = JWTManager(app)


    reqcheck = ReqCheck()
    reqcheck.init_app(app)
    app.register_blueprint(game_bp)
    app.register_blueprint(auth_bp)

    return app
