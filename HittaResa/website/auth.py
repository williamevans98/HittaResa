from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
<<<<<<< Updated upstream:Använd denna/website/auth.py
auth = Blueprint('auth', __name__)

@auth.route('/inloggning', methods=['GET', 'POST'])
=======
import pymysql

# Öppnar anslutningen till databasen.
connection = pymysql.connect(host="sql11.freemysqlhosting.net", user="sql11405569", passwd="8M3yX3fj8V", database="sql11405569")

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Länkar auth.py med main.py
auth = Blueprint('auth', __name__)

# Hämtar alla fält och försöker logga in användaren
@auth.route('/inloggning', methods=['POST'])
>>>>>>> Stashed changes:HittaResa/website/auth.py
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("inloggning.html", user=current_user)

<<<<<<< Updated upstream:Använd denna/website/auth.py
=======
# Loggar ut användaren
>>>>>>> Stashed changes:HittaResa/website/auth.py
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

<<<<<<< Updated upstream:Använd denna/website/auth.py
@auth.route('/registrera.html', methods=['GET', 'POST'])
=======
# Hämtar alla fält och registrerar användaren
@auth.route('/registrera', methods=['POST'])
>>>>>>> Stashed changes:HittaResa/website/auth.py
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords does not match.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("registrera.html", user=current_user)

<<<<<<< Updated upstream:Använd denna/website/auth.py

#En route till gillar-sidan
@auth.route('/gillar')
def gillar():
    return render_template("gillar.html")

#En route till inloggningssidan
=======
# En route till gillar-sidan
@auth.route('/gillar')
def gillar():
    sql = ("SELECT * from images")
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template("gillar.html", user=current_user, content=data)

# En route till inloggningssidan
>>>>>>> Stashed changes:HittaResa/website/auth.py
@auth.route('/inloggning')
def inloggning():
    return render_template("inloggning.html")

<<<<<<< Updated upstream:Använd denna/website/auth.py
#En route till registrera-sidan
=======
# En route till registrera-sidan
>>>>>>> Stashed changes:HittaResa/website/auth.py
@auth.route('/registrera')
def registrera():
    return render_template("registrera.html")

<<<<<<< Updated upstream:Använd denna/website/auth.py
#En route till om-sidan
=======
# En route till om-sidan
>>>>>>> Stashed changes:HittaResa/website/auth.py
@auth.route('/om')
def om():
    return render_template("om.html")