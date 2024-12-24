from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    recipe_description = db.Column(db.String(300), nullable=False)  


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
   
    name = request.form.get('name')
    description = request.form.get('description')

    if not name or not description:
        return jsonify({"error": "Both name and description are required!"}), 400

    
    new_recipe = Recipe(recipe_name=name, recipe_description=description)

    try:
        
        db.session.add(new_recipe)
        db.session.commit()

        return jsonify({"message": "Recipe added successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
