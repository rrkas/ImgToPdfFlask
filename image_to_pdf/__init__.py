from flask import Flask
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    from . import main_routes, error_routes
    app.register_blueprint(main_routes.main_route)
    app.register_blueprint(error_routes.errors)
    return app
