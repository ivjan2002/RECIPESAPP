import unittest
import json
from app import app, db, User
from werkzeug.security import generate_password_hash

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        # Postavljanje aplikacije za testiranje
        self.app = app.test_client()
        self.app.testing = True

        # Kreiranje baze podataka za testiranje
        with app.app_context():
            db.create_all()

        # Dodavanje testnog korisnika u bazu
        test_user = User(
            username='testuser',
            password=generate_password_hash('testpassword')  # Kreiraj hashovane lozinke
        )
        with app.app_context():
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        # Brisanje baze podataka posle testiranja
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_success(self):
        # Testiranje uspešnog login-a
        response = self.app.post('/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', data)  # Očekuje se da token bude prisutan u odgovoru

    def test_login_invalid_credentials(self):
        # Testiranje neuspešnog login-a zbog loših kredencijala
        response = self.app.post('/login', json={
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Invalid username or password')

    def test_login_missing_fields(self):
        # Testiranje neuspešnog login-a zbog nedostajućih polja
        response = self.app.post('/login', json={})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Username and password are required')

if __name__ == '__main__':
    unittest.main()
