from flask import Blueprint, jsonify, request, render_template
from app.models import db, Recipe, User
import jwt
from flask import current_app as app

recipe_bp = Blueprint('recipe', __name__)

def verify_token(token):
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded_token.get('username')
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@recipe_bp.route('/add')
def add_recipe_page():
    return render_template('add_recipe.html', message=None)

@recipe_bp.route('/add_recipe', methods=['POST'])
def add_recipe():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Token is missing!"}), 400

    token = token.split(" ")[1] if " " in token else token
    username = verify_token(token)

    if not username:
        return jsonify({"error": "Invalid or expired token!"}), 401

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User not found!"}), 404

    name = request.form.get('name')
    description = request.form.get('description')

    if not name or not description:
        return jsonify({"error": "Both name and description are required!"}), 400

    new_recipe = Recipe(recipe_name=name, recipe_description=description)

    db.session.add(new_recipe)
    db.session.commit()

    return jsonify({"message": "Recipe added successfully!"}), 201
