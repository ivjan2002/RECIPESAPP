import unittest
import json
from app import app, db, User

class RegisterUserTestCase(unittest.TestCase):
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

    def test_register_user_success(self):
        # Testiranje uspešne registracije korisnika
        response = self.app.post('/register', json={
            "First_name": "John",
            "Last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Korisnik uspešno registrovan!")

        # Provera da li je korisnik dodat u bazu
        with app.app_context():
            user = User.query.filter_by(username="johndoe").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, "johndoe@example.com")

    def test_register_user_missing_fields(self):
        # Testiranje neuspešne registracije zbog nedostajućih polja
        response = self.app.post('/register', json={
            "First_name": "John",
            "Last_name": "Doe",
            "username": "johndoe"
            # Nedostaju email i password
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Sva polja su obavezna!")

    def test_register_user_password_mismatch(self):
        # Testiranje neuspešne registracije zbog nepoklapanja šifri
        response = self.app.post('/register', json={
            "First_name": "John",
            "Last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "password123",
            "confirm_password": "password456"  # Šifre se ne podudaraju
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Šifre se ne podudaraju!")

    def test_register_user_existing_user(self):
        # Testiranje neuspešne registracije zbog postojećeg korisnika
        with app.app_context():
            # Dodavanje postojećeg korisnika u bazu
            existing_user = User(
                First_name="John",
                Last_name="Doe",
                username="johndoe",
                email="johndoe@example.com",
                password="hashed_password"
            )
            db.session.add(existing_user)
            db.session.commit()

        response = self.app.post('/register', json={
            "First_name": "John",
            "Last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "password123",
            "confirm_password": "password123"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", data)
        self.assertEqual(data["message"], "Korisnik sa tim korisničkim imenom ili emailom već postoji!")

if __name__ == '__main__':
    unittest.main()
