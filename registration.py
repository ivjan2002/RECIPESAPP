from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracija baze podataka
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model za korisnika (sa novim kolonama)
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(50), nullable=False)
    Last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

# Ruta za registraciju korisnika
@app.route('/register', methods=['POST'])
def register_user():
    # Preuzimanje podataka iz zahteva
    data = request.get_json()
    first_name = data.get('First_name')
    last_name = data.get('Last_name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    
    # Validacija podataka
    if not all([first_name, last_name, username, email, password, confirm_password]):
        return jsonify({"message": "Sva polja su obavezna!"}), 400
    
    if password != confirm_password:
        return jsonify({"message": "Šifre se ne podudaraju!"}), 400

    # Provera da li korisnik već postoji
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"message": "Korisnik sa tim korisničkim imenom ili emailom već postoji!"}), 400

    # Hashovanje šifre
    hashed_password = generate_password_hash(password)

    # Kreiranje korisnika
    new_user = User(First_name=first_name, Last_name=last_name, username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Korisnik uspešno registrovan!"}), 201

# Pokretanje aplikacije
if __name__ == '__main__':
    # Kreiranje tabela (ako ne postoje)
    #with app.app_context():
        #db.create_all()
    app.run(debug=True)
