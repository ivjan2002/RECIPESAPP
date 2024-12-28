from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Konfiguracija baze podataka
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model za korisnika
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    sifra = db.Column(db.String(50), nullable=False)

# Ruta za registraciju korisnika
@app.route('/register', methods=['POST'])
def register_user():
    # Preuzimanje podataka iz zahteva
    data = request.get_json()
    ime = data.get('ime')
    prezime = data.get('prezime')
    username = data.get('username')
    email = data.get('email')
    sifra = data.get('sifra')
    potvrda_sifre = data.get('potvrda_sifre')
    
    # Validacija podataka
    if not all([ime, prezime, username, email, sifra, potvrda_sifre]):
        return jsonify({"message": "Sva polja su obavezna!"}), 400
    
    if sifra != potvrda_sifre:
        return jsonify({"message": "Šifre se ne podudaraju!"}), 400

    # Provera da li korisnik već postoji
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"message": "Korisnik sa tim korisničkim imenom ili emailom već postoji!"}), 400

    # Hashovanje šifre
    hashed_password = generate_password_hash(sifra)

    # Kreiranje korisnika
    new_user = User(ime=ime, prezime=prezime, username=username, email=email, sifra=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Korisnik uspešno registrovan!"}), 201

# Pokretanje aplikacije
if __name__ == '__main__':
    # Kreiranje tabela (ako ne postoje)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
