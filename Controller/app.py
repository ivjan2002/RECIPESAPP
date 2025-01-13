from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template


app=Flask(__name__,template_folder=r'C:\Users\IVANA\recipesApp\frontEndTemplates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

class Recipe(db.Model):
    __tablename__='recipes'

    recipe_id = db.Column(db.Integer, primary_key=True) 
    recipe_name = db.Column(db.String(50), nullable=False)
    recipe_description = db.Column(db.String(300), nullable=False)

@app.route('/recipes', methods=['GET'])
def get_recipes():
    
    recipes = Recipe.query.with_entities(Recipe.recipe_name, Recipe.recipe_description).all()
    
    
    recipes_list = [{'name': r.recipe_name, 'description': r.recipe_description} for r in recipes]
    
    #return jsonify(recipes_list)
    return render_template('explore_recipe.html', recipes=recipes_list)

if __name__ == '__main__':
    app.run(debug=True)

