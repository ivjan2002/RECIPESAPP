import unittest
from app import app, db, User
from werkzeug.security import generate_password_hash

class LoginTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Konfiguracija za testiranje sa MySQL bazom
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
        app.config['TESTING'] = True
        cls.client = app.test_client()

        with app.app_context():
            # Dodaj korisnika za testiranje
            hashed_password = generate_password_hash("password123")
            user = User(username="testuser", password=hashed_password)
            db.session.add(user)
            db.session.commit()

    @classmethod
    def tearDownClass(cls):
        # Očisti korisnike nakon testova
        with app.app_context():
            user = User.query.filter_by(username="testuser").first()
            if user:
                db.session.delete(user)
                db.session.commit()

    def test_login_success(self):
        # Testiranje uspešnog logina
        response = self.client.post('/login', data=dict(
            username="testuser",
            password="password123"
        ))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('token', data)

    def test_login_invalid_credentials(self):
        # Testiranje neuspešnog logina sa lošim podacima
        response = self.client.post('/login', data=dict(
            username="testuser",
            password="wrongpassword"
        ))
        self.assertEqual(response.status_code, 401)
        data = response.get_json()
        self.assertEqual(data['error'], 'Invalid username or password')

    def test_login_missing_fields(self):
        # Testiranje greške kad nedostaju obavezna polja
        response = self.client.post('/login', data=dict(
            username="testuser"
        ))
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Username and password are required')

        response = self.client.post('/login', data=dict(
            password="password123"
        ))
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Username and password are required')

if __name__ == '__main__':
    unittest.main()
