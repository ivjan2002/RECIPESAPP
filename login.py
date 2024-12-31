from flask import Flask, request, jsonify
import jwt
import datetime
from werkzeug.security import check_password_hash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Konfiguracija baze podataka i tajni ključ
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'

db = SQLAlchemy(app)

# Model korisnika
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Funkcija za generisanje JWT tokena
def generate_jwt(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")
    return token

# Ruta za login
@app.route('/login', methods=['POST'])
def login():
    data = request.json

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Username and password are required"}), 400

    username = data['username']
    password = data['password']

    # Provera korisnika u bazi
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Generisanje tokena
    token = generate_jwt(username)
    return jsonify({"token": token})

if __name__ == '__main__':
    app.run(debug=True)
