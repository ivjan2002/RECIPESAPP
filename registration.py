from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import render_template

app = Flask(__name__,template_folder=r'C:\Users\IVANA\recipesApp\frontEndTemplates')


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/recipesdatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(50), nullable=False)
    Last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)


@app.route('/reg')
def index():
    return render_template('register.html',message=None)



@app.route('/register', methods=['POST'])
def register_user():
    
    
    first_name =request.form.get('First_name')
    last_name =request.form.get('Last_name')
    username =request.form.get('username')
    email =request.form.get('email')
    password =request.form.get('password')
    confirm_password =request.form.get('confirm_password')
    
    
    if not all([first_name, last_name, username, email, password, confirm_password]):
        return jsonify({"message": "Sva polja su obavezna!"}), 400
    
    if password != confirm_password:
        return jsonify({"message": "Šifre se ne podudaraju!"}), 400

    
    existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
    if existing_user:
        return jsonify({"message": "Korisnik sa tim korisničkim imenom ili emailom već postoji!"}), 400

    
    hashed_password = generate_password_hash(password)

    
    new_user = User(First_name=first_name, Last_name=last_name, username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Korisnik uspešno registrovan!"}), 201


if __name__ == '__main__':
    app.run(debug=True)
