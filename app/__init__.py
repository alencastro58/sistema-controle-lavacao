from flask import Flask

from .config import Config
from .extensions import db

from .routes.cliente_web import cliente_web_bp
from .routes.dashboard import dashboard_bp
from .routes.health import health_bp
from .routes.home import home_bp
from .routes.lavagem import lavagem_bp
from .routes.ordem_servico import ordem_servico_bp
from .routes.ordem_servico_web import ordem_servico_web_bp
from .routes.preco_servico import preco_servico_bp
from .routes.servico_web import servico_web_bp
from .routes.veiculo_web import veiculo_web_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.register_blueprint(home_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(lavagem_bp)
    app.register_blueprint(ordem_servico_bp)
    app.register_blueprint(ordem_servico_web_bp)
    app.register_blueprint(cliente_web_bp)
    app.register_blueprint(veiculo_web_bp)
    app.register_blueprint(servico_web_bp)
    app.register_blueprint(preco_servico_bp)

    return app
