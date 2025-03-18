from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

class Recipe(db.Model):
    __tablename__ = 'recipes'
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    recipe_description = db.Column(db.String(300), nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    user = db.relationship('User', backref='recipes', lazy=True)

