from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
import jwt

app = Flask(__name__,template_folder=r'C:\Users\IVANA\recipesApp\frontEndTemplates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    recipe_description = db.Column(db.String(300), nullable=False)

def verify_token(token):
    if not isinstance(token, str):
        raise TypeError("Expected a string value for token")
    try:
        decoded_token = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        return decoded_token['username']
    except jwt.ExpiredSignatureError:
        return None 
    except jwt.InvalidTokenError:
        return None 

@app.route('/delete')
def index():
    return render_template('deleterecipe.html',message=None)

@app.route('/delete_recipe', methods=['DELETE'])
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


if __name__ == '__main__':
    app.run(debug=True)
