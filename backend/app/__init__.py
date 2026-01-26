import os
from flask import Flask
from backend.app.config import Config
from backend.app.extensions import cors
from backend.app.routes.products import product_bp


def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "..", "..", "frontend", "templates"),
                static_folder=os.path.join(BASE_DIR, "..", "..", "frontend", "static"), static_url_path="/static")
    app.config.from_object(Config)

    cors.init_app(app)

    app.register_blueprint(product_bp)

    return app
