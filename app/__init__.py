from flask import Flask, render_template

from config import config
from .extensions import db
from app.models import Item, User


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .routes import main_bp

    app.register_blueprint(main_bp)

    register_error_handlers(app)

    @app.context_processor
    def inject_globals():
        return {"app_name": app.config["APP_NAME"]}

    with app.app_context():
        from . import models  # noqa: F401

        db.create_all()

    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(_e):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(_e):
        return render_template("500.html"), 500
