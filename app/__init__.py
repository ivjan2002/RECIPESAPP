from flask import Flask
from app.config import Config
from app.models import db
from app.auth_routes import auth_bp
from app.recipe_routes import recipe_bp

def create_app():
    app = Flask(__name__, template_folder=r'C:\Users\IVANA\recipesApp\frontEndTemplates')
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)

    return app
