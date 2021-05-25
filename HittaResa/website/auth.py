from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import pymysql
from db_connection import *

connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)


# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Länkar auth.py med main.py
auth = Blueprint('auth', __name__)

@auth.route('/inloggning', methods=['GET', 'POST'])
def login():
    '''
    Hämtar alla fält och försöker logga in användaren
    '''
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Inloggningen lyckades!', category='success')
                login_user(user, remember=False, fresh=True)
                connection.close()
                return redirect(url_for('views.home'))
            else:
                flash('Felaktigt lösenord, försök igen', category='error')
        else:
            flash('E-postadressen finns inte registrerad', category='error')

    connection.close()
    return render_template("inloggning.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    '''
    Loggar ut användaren
    '''
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
    logout_user()
    connection.close()
    return redirect(url_for('views.home'))

@auth.route('/registrera', methods=['POST'])
def sign_up():
    '''
    Hämtar alla fält och registrerar användaren
    '''
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
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
        connection.close()
        return redirect(url_for('views.home'))
    connection.close()
    return render_template("registrera.html")

@auth.route('/gillar', methods=['GET', 'POST'])
def gillar():
    '''
    En route till gillar-sidan

    Om man väljer att söka på ett resmål visas det upp annars visas alla resmålen man gillat
    
    '''
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
    cursor = connection.cursor()
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
            connection.close()
            return render_template("gillar.html", user=current_user, content=data)
        except:
            connection.close()
            return render_template("gillar.html", user=current_user, content=data)
    else:
        sql = ("SELECT * FROM images JOIN status on images.image_id = status.image_id WHERE like_or_not = 1 AND user_id = " + get_user_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        connection.close()
        return render_template("gillar.html", user=current_user, content=data)

@auth.route('/inloggning')
def inloggning():
    '''
    En route till inloggningssidan.
    '''
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
    connection.close()
    return render_template("inloggning.html")

@auth.route('/registrera')
def registrera():
    '''
    En route till registrera-sidan.
    '''
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
    connection.close()
    return render_template("registrera.html")

@auth.route('/om')
def om():
    '''
    En route till om-sidan.
    '''
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
    connection.close()
    return render_template("om.html")

@auth.route('/like', methods=['POST'])
def image_like_or_not():
    '''
    En route för att spara en gillning, utan att returnera en template.
    '''
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
    cursor = connection.cursor()
    location = request.form['data']
    string = str(current_user)
    get_last_element = string.split(' ')[-1]
    get_user_id = get_last_element.strip('>')
    sql = "select image_id from images where location = '" + location + "'"
    cursor.execute(sql)
    id = cursor.fetchone()[0]
    status_like = "1"
    
    # Kolla om det finns en aktiv användare och ett användarid    
    if current_user.is_active and get_user_id != "":
        # Kolla om bilden redan finns i tabellen
        cursor.execute("SELECT * from status where user_id = " + str(get_user_id) + "  and image_id = " + str(id))
        exists = cursor.fetchone()
            
        if exists is None:
            # Bilden finns inte i tabellen, lägg in den med insert
            cursor.execute("INSERT INTO status (user_id, image_id, like_or_not) values(" + str(get_user_id) + ", " + str(id) + ", " + str(status_like) + ")")
            connection.commit()
        else:
            # Bilden finns i tabellen, uppdatera like_or_not till 1
            cursor.execute("UPDATE status set like_or_not = " + str(status_like) + " where user_id = " + str(get_user_id) + " and image_id = " + str(id))

    connection.close()
    return "done"

@auth.route('/remove', methods=['POST'])
def remove_image_like():
    '''
    En route för att ta bort en gillning, redirectar sedan till /gillar-sidan.
    '''
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
    cursor = connection.cursor()
    location = request.form['img-title']
    string = str(current_user)
    get_last_element = string.split(' ')[-1]
    get_user_id = get_last_element.strip('>')
    sql = "select image_id from images where location = '" + location + "'"
    cursor.execute(sql)
    id = cursor.fetchone()[0]
    status_like = "0"
    if get_user_id != "":
        cursor.execute("UPDATE status set like_or_not = " + str(status_like) + " where user_id = " + str(get_user_id) + " and image_id = " + str(id) + "")
        connection.commit()
    else:
        pass
    connection.close()
    return redirect(url_for('auth.gillar'))