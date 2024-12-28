from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model korisnika
class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Ne koristi plain text lozinke u stvarnim aplikacijama

    # Veza sa receptima
    recipes = db.relationship('Recipe', backref='owner', lazy=True)

# Model recepta
class Recipe(db.Model):
    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    recipe_description = db.Column(db.String(300), nullable=False)
    
    # Spoljni ključ koji povezuje recept sa korisnikom
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

@app.route('/recipes', methods=['GET'])
def get_user_recipes():
    # Pretpostavljamo da je korisnik autentifikovan i da imamo ID korisnika (npr. iz JWT tokena ili sesije)
    user_id = request.args.get('user_id')  # Uzimamo ID korisnika iz URL parametra (može biti i iz headera ili tokena)

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    # Pronalazi sve recepte tog korisnika
    user_recipes = Recipe.query.filter_by(user_id=user_id).all()

    # Ako korisnik nema recepte
    if not user_recipes:
        return jsonify({"message": "No recipes found for this user."}), 404

    # Kreiranje liste sa receptima korisnika
    recipes_list = [{'name': r.recipe_name, 'description': r.recipe_description} for r in user_recipes]

    return jsonify(recipes_list)

if __name__ == '__main__':
    app.run(debug=True)
