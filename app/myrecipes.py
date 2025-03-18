from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
import jwt

app = Flask(__name__, template_folder=r'C:\Users\IVANA\recipesApp\frontEndTemplates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here' 

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(50), nullable=False)
    Last_name = db.Column(db.String(50), nullable=False)
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

@app.route('/myrecipes', methods=['GET'])
def get_recipes():
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

if __name__ == '__main__':
    app.run(debug=True)
