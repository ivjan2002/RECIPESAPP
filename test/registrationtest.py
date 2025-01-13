import unittest
from app import app, db, User

class RegisterTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Set up the test client and initialize the database
        cls.app = app.test_client()
        cls.app.testing = True
        
        # Create all tables for testing
        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        # Drop all tables after tests
        with app.app_context():
            db.drop_all()

    def test_register_success(self):
        # Test successful registration
        response = self.app.post('/register', data=dict(
            First_name="John",
            Last_name="Doe",
            username="john_doe",
            email="john.doe@example.com",
            password="password123",
            confirm_password="password123"
        ))
        json_response = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response["message"], "Korisnik uspešno registrovan!")

    def test_register_missing_fields(self):
        # Test registration with missing fields
        response = self.app.post('/register', data=dict(
            First_name="John",
            Last_name="Doe",
            username="john_doe",
            email="john.doe@example.com",
            password="password123",
            confirm_password=""
        ))
        json_response = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Sva polja su obavezna!")

    def test_register_password_mismatch(self):
        # Test registration where passwords don't match
        response = self.app.post('/register', data=dict(
            First_name="John",
            Last_name="Doe",
            username="john_doe",
            email="john.doe@example.com",
            password="password123",
            confirm_password="password321"
        ))
        json_response = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Šifre se ne podudaraju!")

    def test_register_existing_user(self):
        # Test registration where username or email already exists
        with app.app_context():
            user = User(First_name="Jane", Last_name="Doe", username="existing_user",  password="hashed_password",email="existing@example.com")
            db.session.add(user)
            db.session.commit()
        
        response = self.app.post('/register', data=dict(
            First_name="John",
            Last_name="Doe",
            username="existing_user",
            email="existing@example.com",
            password="password123",
            confirm_password="password123"
        ))
        json_response = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response["message"], "Korisnik sa tim korisničkim imenom ili emailom već postoji!")

if __name__ == '__main__':
    unittest.main()
