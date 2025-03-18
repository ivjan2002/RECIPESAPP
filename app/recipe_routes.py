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

@recipe_bp.route('/delete')
def delete_recipe_page():
    return render_template('deleterecipe.html',message=None)

@recipe_bp.route('/delete_recipe', methods=['DELETE'])
def delete_recipe():
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
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({"error": "Recipe name is required!"}), 400

    
    recipe_to_delete = Recipe.query.filter_by(recipe_name=name).first()

    if not recipe_to_delete:
        return jsonify({"error": "Recipe not found!"}), 404

    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return jsonify({"message": f"Recipe '{name}' deleted successfully!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@recipe_bp.route('/explore_recipes', methods=['GET'])
def get_recipes():
    
    recipes = Recipe.query.with_entities(Recipe.recipe_name, Recipe.recipe_description).all()
    
    
    recipes_list = [{'name': r.recipe_name, 'description': r.recipe_description} for r in recipes]
    

    return render_template('explore_recipe.html', recipes=recipes_list)

@recipe_bp.route('/myrecipes', methods=['GET'])
def get_my_recipes():
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

    
    recipes = Recipe.query.filter_by(user_id=user.user_id).all()

    
    recipes_list = [{'name': r.recipe_name, 'description': r.recipe_description} for r in recipes]

  
    return render_template('myrecipe.html', recipes=recipes_list)