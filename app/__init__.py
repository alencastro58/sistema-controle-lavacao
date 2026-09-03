from flask import Flask

from .config import Config
from .extensions import db
from .routes.health import health_bp
from .routes.lavagem import lavagem_bp
from .routes.ordem_servico import ordem_servico_bp
from . import models


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(health_bp)
    app.register_blueprint(lavagem_bp)
    app.register_blueprint(ordem_servico_bp)

    return app
