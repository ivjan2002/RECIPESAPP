from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)

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
    if any(user['username'] == username or user['email'] == email for user in db):
        return jsonify({"message": "Korisnik sa tim korisničkim imenom ili emailom već postoji!"}), 400

    # Hashovanje šifre
    hashed_password = generate_password_hash(sifra)

    # Kreiranje korisnika
    new_user = {
        "ime": ime,
        "prezime": prezime,
        "username": username,
        "email": email,
        "sifra": hashed_password
    }
    db.append(new_user)

    return jsonify({"message": "Korisnik uspešno registrovan!"}), 201

if __name__ == '__main__':
    app.run(debug=True)
