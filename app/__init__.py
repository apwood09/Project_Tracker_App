from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name="default"): 
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "super-secret-knitting-key" # secure sessions 

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
    app.register_blueprint(main_bp, url_prefix='/api')

    return app 