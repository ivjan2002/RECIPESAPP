import unittest
import json
from deleterecipe import app, db, Recipe

class GetRecipesTestCase(unittest.TestCase):
    def setUp(self):
        # Postavljanje aplikacije za testiranje
        self.app = app.test_client()
        self.app.testing = True

        # Kreiranje baze podataka za testiranje
        with app.app_context():
            db.create_all()

            # Dodavanje testnih recepata
            recipe1 = Recipe(recipe_name="Spaghetti Bolognese", recipe_description="Traditional Italian pasta dish.")
            recipe2 = Recipe(recipe_name="Chicken Curry", recipe_description="Spicy and flavorful curry.")
            db.session.add(recipe1)
            db.session.add(recipe2)
            db.session.commit()

    def tearDown(self):
        # Brisanje baze podataka posle testiranja
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_recipes(self):
        # Testiranje GET metode za recepte
        response = self.app.get('/recipes')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 2)  # Proverava da li ima 2 recepta
        self.assertEqual(data[0]['name'], "Spaghetti Bolognese")
        self.assertEqual(data[1]['name'], "Chicken Curry")
        self.assertEqual(data[0]['description'], "Traditional Italian pasta dish.")
        self.assertEqual(data[1]['description'], "Spicy and flavorful curry.")

if __name__ == '__main__':
    unittest.main()
