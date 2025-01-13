import unittest
import json
from app import app, db, Recipe

class DeleteRecipeTestCase(unittest.TestCase):
    def setUp(self):
        # Postavljanje aplikacije za testiranje
        self.app = app.test_client()
        self.app.testing = True

        # Kreiranje baze podataka za testiranje
        with app.app_context():
            db.create_all()

            # Dodavanje testnog recepta
            test_recipe = Recipe(recipe_name='Test Recipe', recipe_description='Test Description')
            db.session.add(test_recipe)
            db.session.commit()

    def tearDown(self):
        # Brisanje baze podataka posle testiranja
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_delete_recipe_success(self):
        # Testiranje uspešnog brisanja recepta
        response = self.app.delete('/delete_recipe', json={
            'name': 'Test Recipe'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', data)
        self.assertEqual(data['message'], "Recipe 'Test Recipe' deleted successfully!")

        # Proveravanje da li je recept obrisan iz baze
        with app.app_context():
            recipe = Recipe.query.filter_by(recipe_name='Test Recipe').first()
            self.assertIsNone(recipe)

    def test_delete_recipe_missing_name(self):
        # Testiranje neuspešnog brisanja zbog nedostatka imena recepta
        response = self.app.delete('/delete_recipe', json={})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Recipe name is required!')

    def test_delete_recipe_not_found(self):
        # Testiranje neuspešnog brisanja kada recept ne postoji
        response = self.app.delete('/delete_recipe', json={
            'name': 'Nonexistent Recipe'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Recipe not found!')

    def test_delete_recipe_database_error(self):
        # Simulacija greške baze podataka
        with app.app_context():
            db.session.remove()

        response = self.app.delete('/delete_recipe', json={
            'name': 'Test Recipe'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 500)
        self.assertIn('error', data)
        self.assertTrue('An error occurred' in data['error'])

if __name__ == '__main__':
    unittest.main()
