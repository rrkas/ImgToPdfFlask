from flask import Flask, url_for
from .config import Config


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))

    from . import main_routes, error_routes
    app.register_blueprint(main_routes.main_route)
    app.register_blueprint(error_routes.errors)
    return app
