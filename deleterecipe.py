from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__,template_folder=r'C:\Users\IVANA\recipesApp\frontEndTemplates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Recipe(db.Model):
    __tablename__ = 'recipes'

    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    recipe_description = db.Column(db.String(300), nullable=False)

@app.route('/delete')
def index():
    return render_template('deleterecipe.html',message=None)

@app.route('/delete_recipe', methods=['DELETE'])
def delete_recipe():
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
