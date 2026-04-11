from flask import Flask
from web.route.routes import game_bp


def create_app(storage):
    app = Flask(__name__)
    app.register_blueprint(game_bp)

    return app
