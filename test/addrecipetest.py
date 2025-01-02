import unittest
import json
from app import app, db, Recipe

class AddRecipeTestCase(unittest.TestCase):
    def setUp(self):
        # Postavljanje aplikacije za testiranje
        self.app = app.test_client()
        self.app.testing = True

        # Kreiranje baze podataka za testiranje
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Brisanje baze podataka posle testiranja
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_recipe_success(self):
        # Testiranje uspešnog dodavanja recepta
        response = self.app.post('/add_recipe', json={
            'name': 'Pasta Carbonara',
            'description': 'A classic Italian pasta dish with eggs, cheese, pancetta, and pepper.'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Recipe added successfully!')

        # Proveravanje da li je recept dodat u bazu
        with app.app_context():
            recipe = Recipe.query.filter_by(recipe_name='Pasta Carbonara').first()
            self.assertIsNotNone(recipe)
            self.assertEqual(recipe.recipe_description, 'A classic Italian pasta dish with eggs, cheese, pancetta, and pepper.')

    def test_add_recipe_missing_fields(self):
        # Testiranje neuspešnog dodavanja recepta zbog nedostajućih polja
        response = self.app.post('/add_recipe', json={})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Both name and description are required!')

    def test_add_recipe_database_error(self):
        # Simulacija greške baze podataka
        with app.app_context():
            db.session.remove()  

        response = self.app.post('/add_recipe', json={
            'name': 'Pasta Carbonara',
            'description': 'A classic Italian pasta dish with eggs, cheese, pancetta, and pepper.'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)
        self.assertTrue('An error occurred' in data['error'])

if __name__ == '__main__':
    unittest.main()
