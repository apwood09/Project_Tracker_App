from flask import Flask 
from app.extensions import db, login_manager

def create_app(config_name="default"): 
    app = Flask(__name__)
    # configuration settings 
    app.config["SECRET_KEY"] = "super-secret-knitting-key" # secure sessions 
    # db URI 
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    # initialize extensions 
    db.init_app(app)
    login_manager.init_app(app)

    # configure session security level 
    login_manager.session_protection = "strong"

    # User loader callback: find user by ID 
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id): 
        return User.query.get(int(user_id))
    
    # register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app 