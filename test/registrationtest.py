import unittest
from app import app  # Importuj Flask aplikaciju

class RegisterTestCase(unittest.TestCase):

    # Postavljanje testnog klijenta
    def setUp(self):
        self.client = app.test_client()  # Flask test klijent

    # Testiranje uspešne registracije
    def test_register_success(self):
        response = self.client.post('/register', data={
            'username': 'new_user',
            'password': 'new_password123'
        })
        self.assertEqual(response.status_code, 302)  # Očekujemo redirekciju
        self.assertIn('User registered successfully', response.data.decode('utf-8'))

    # Testiranje već postojećeg korisnika
    def test_register_existing_user(self):
        # Registrujemo prvog korisnika
        self.client.post('/register', data={
            'username': 'existing_user',
            'password': 'password123'
        })
        
        # Pokušaj registracije sa istim korisničkim imenom
        response = self.client.post('/register', data={
            'username': 'existing_user',
            'password': 'new_password123'
        })
        self.assertEqual(response.status_code, 302)  # Očekujemo redirekciju
        self.assertIn('User already exists', response.data.decode('utf-8'))

    # Testiranje nedostajućih polja
    def test_register_missing_fields(self):
        response = self.client.post('/register', data={
            'username': 'incomplete_user'
            # Nedostaje lozinka
        })
        self.assertEqual(response.status_code, 302)  # Očekujemo redirekciju
        self.assertIn('Username and password are required', response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
