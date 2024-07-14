from flask import Flask
from config import config
from .routes import main
import os

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])


    # Register the Blueprint
    app.register_blueprint(main)

    return app