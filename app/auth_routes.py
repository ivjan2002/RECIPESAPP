from flask import Blueprint, request, jsonify, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User
import jwt
import datetime
from flask import current_app as app

auth_bp = Blueprint('auth', __name__)

def generate_jwt(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

@auth_bp.route('/log')
def login_page():
    return render_template('login.html', message=None)

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_jwt(username)
    return jsonify({"token": token})

@auth_bp.route('/reg')
def register_page():
    return render_template('register.html', message=None)

@auth_bp.route('/register', methods=['POST'])
def register_user():
    first_name = request.form.get('First_name')
    last_name = request.form.get('Last_name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if not all([first_name, last_name, username, email, password, confirm_password]):
        return jsonify({"message": "Sva polja su obavezna!"}), 400

    if password != confirm_password:
        return jsonify({"message": "Šifre se ne podudaraju!"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "Korisnik već postoji!"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(first_name=first_name, last_name=last_name, username=username, email=email, password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Korisnik uspešno registrovan!"}), 201
