# app/__init__.py
from flask import Flask
from flask_cors import CORS
from .routes import stock_bp
from config import Config


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(stock_bp)
    app.config.from_object(Config)

    # Import blueprints, extensions, etc.

    return app
