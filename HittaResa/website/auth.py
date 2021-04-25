from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import pymysql

# Öppnar anslutningen till databasen.
connection = pymysql.connect(host="sql11.freemysqlhosting.net",
                             user="sql11405569", passwd="8M3yX3fj8V", database="sql11405569")

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Länkar auth.py med main.py
auth = Blueprint('auth', __name__)

# Hämtar alla fält och försöker logga in användaren


@auth.route('/inloggning', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Inloggningen lyckades!', category='success')
                login_user(user, remember=False, fresh=True)
                return redirect(url_for('views.home'))
            else:
                flash('Felaktigt lösenord, försök igen', category='error')
        else:
            flash('Email finns inte', category='error')

    return render_template("inloggning.html", user=current_user)

# Loggar ut användaren


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

# Hämtar alla fält och registrerar användaren


@auth.route('/registrera', methods=['POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email finns redan', category='error')
        elif len(email) < 4:
            flash('Email måste bestå av mer än 3 bokstäver', category='error')
        elif len(first_name) < 2:
            flash('Förnamnet måste vara längre än 1 bokstav', category='error')
        elif password1 != password2:
            flash('Lösenord matchar inte', category='error')
        elif len(password1) < 8:
            flash('Lösenordet måste vara mer än 8 karaktärer', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=False)
            flash('Konto skapat!', category='success')
            return redirect(url_for('views.home'))

    return render_template("registrera.html")

# En route till gillar-sidan
# Om man väljer att söka på ett resmål visas det upp annars visas alla resmålen man gillat


@auth.route('/gillar', methods=['GET', 'POST'])
def gillar():
    if request.method == "POST":
        print(request.form['search'])
        search = request.form['search']
        sql = """SELECT * FROM images WHERE location = '%s'""" % (search)
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template("gillar.html", user=current_user, content=data)
    else:
        sql = ("SELECT * from images")
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template("gillar.html", user=current_user, content=data)

# En route till inloggningssidan


@auth.route('/inloggning')
def inloggning():
    return render_template("inloggning.html")

# En route till registrera-sidan


@auth.route('/registrera')
def registrera():
    return render_template("registrera.html")

# En route till om-sidan


@auth.route('/om')
def om():
    return render_template("om.html")
