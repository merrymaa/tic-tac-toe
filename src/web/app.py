from flask import Flask
from web.route.game_routes import game_bp
from web.route.auth_routes import auth_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(game_bp)
    app.register_blueprint(auth_bp)

    return app
