from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import pymysql
import pyodbc as db

server = 'localhost'
username = 'TestUser'
password = 'a'
database = 'HittaResa'
connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' +
                        database + ';UID=' + username + ';PWD=' + password)

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
            flash('E-postadressen finns inte registrerad', category='error')

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
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('E-postadressen finns redan registrerad', category='error')
        elif len(email) < 4:
            flash('E-postadressen måste bestå av minst 4 tecken', category='error')
        elif password1 != password2:
            flash('Lösenord matchar inte', category='error')
        elif len(password1) < 8:
            flash('Lösenordet måste bestå av minst 8 tecken', category='error')
        else:
            new_user = User(email=email, password=generate_password_hash(
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
    string = str(current_user)
    get_last_element = string.split(' ')[-1]
    get_user_id = get_last_element.strip('>')
    print(get_user_id)
    if request.method == "POST":
        print(request.form['search'])
        search = request.form['search']
        try:
            sql = ("SELECT * FROM images JOIN status on images.image_id = status.image_id WHERE like_or_not = 1 AND user_id = " + get_user_id + " AND location = '%s'" % (search))
            cursor.execute(sql)
            data = cursor.fetchall()
            return render_template("gillar.html", user=current_user, content=data)
            connection.close()
        except:
            return render_template("gillar.html", user=current_user, content=data)
            connection.close()
    else:
        sql = ("SELECT * FROM images JOIN status on images.image_id = status.image_id WHERE like_or_not = 1 AND user_id = " + get_user_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        return render_template("gillar.html", user=current_user, content=data)
        connection.close()

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

# En route för att spara en gillning, utan att returnera en template
@auth.route('/like', methods=['POST'])
def image_like_or_not():
    if request.method == 'POST':
        location = request.form['data']
        string = str(current_user)
        get_last_element = string.split(' ')[-1]
        get_user_id = get_last_element.strip('>')
        sql = "select image_id from images where location = '" + location + "'"
        cursor.execute(sql)
        id = cursor.fetchone()[0]
        status_like = "1"
    
        if get_user_id != "":
            # Kolla om bilden redan finns i tabellen
            cursor.execute("SELECT * from status where user_id = ? and image_id = ?", get_user_id, id)
            exists = cursor.fetchone()
            
            if exists is None:
                # Bilden finns inte i tabellen, lägg in den med insert
                cursor.execute("INSERT INTO status (user_id, image_id, like_or_not) values(?, ?, ?)", get_user_id, id, status_like)
                connection.commit()
            else:
                # Bilden finns i tabellen, uppdatera like_or_not till 1
                cursor.execute("UPDATE status set like_or_not = ? where user_id = ? and image_id = ?", status_like, get_user_id, id)
                connection.commit()
        
        return "done"

# En route för att ta bort en gillning, redirectar sedan till /gillar-sidan
@auth.route('/remove', methods=['POST'])
def remove_image_like():
    if request.method == 'POST':
        location = request.form['img-title']
        string = str(current_user)
        get_last_element = string.split(' ')[-1]
        get_user_id = get_last_element.strip('>')
        sql = "select image_id from images where location = '" + location + "'"
        cursor.execute(sql)
        id = cursor.fetchone()[0]
        status_like = "0"
        if get_user_id != "":
            cursor.execute("UPDATE status set like_or_not = ? where user_id = ? and image_id = ?", status_like, get_user_id, id)
            connection.commit()
        else:
            pass
        return redirect(url_for('auth.gillar'))