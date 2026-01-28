import os
from flask import Flask
from backend.app.config import Config
from backend.app.extensions import cors
from backend.app.routes.products import product_bp
from backend.app.routes.cart import cart_bp
from backend.app.routes.orders import orders_bp
from backend.app.routes.auth import auth_bp
from backend.app.routes.pages import pages_bp


def create_app():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "..", "..", "frontend", "templates"),
                static_folder=os.path.join(BASE_DIR, "..", "..", "frontend", "static"), static_url_path="/static")
    app.config.from_object(Config)

    cors.init_app(app)

    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(pages_bp)

    return app
