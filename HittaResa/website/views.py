# Import av funktioner som vi använder
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import pymysql
from db_connection import *
import pyodbc as db

# Öppnar anslutningen till databasen.
server = 'localhost'
username = 'TestUser'
password = 'a'
database = 'HittaResa'
connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' +
                        database + ';UID=' + username + ';PWD=' + password)

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Definierar views som blueprints för att vi ska kunna använda det som templates
views = Blueprint('views', __name__)

# Routar hem när de är inloggade
@views.route('/', methods=['GET', 'POST'])  

# Hämtar bild-länken från databasen och returnerar den som "data"
def home():
    string = str(current_user)
    get_last_element = string.split(' ')[-1]
    get_user_id = get_last_element.strip('>')
    print(get_user_id)
    sql = ("SELECT * FROM images WHERE NOT EXISTS (SELECT * FROM status WHERE status.image_id = images.image_id AND status.user_id = " + get_user_id + ") order by newid()")
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template("index.html", user=current_user, content=data)
    connection.close()