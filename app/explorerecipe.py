from flask import Flask,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask import render_template
from app import app,db,Recipe


@app.route('/recipes', methods=['GET'])
def get_recipes():
    
    recipes = Recipe.query.with_entities(Recipe.recipe_name, Recipe.recipe_description).all()
    
    
    recipes_list = [{'name': r.recipe_name, 'description': r.recipe_description} for r in recipes]
    
    #return jsonify(recipes_list)
    return render_template('explore_recipe.html', recipes=recipes_list)

if __name__ == '__main__':
    app.run(debug=True)

