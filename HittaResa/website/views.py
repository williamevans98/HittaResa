# Import av funktioner som vi använder
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
import pymysql

# Öppnar anslutningen till databasen.
connection = pymysql.connect(host="sql11.freemysqlhosting.net", user="sql11405569", passwd="8M3yX3fj8V", database="sql11405569")

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Definierar views som blueprints för att vi ska kunna använda det som templates
views = Blueprint('views', __name__)

# Routar hem när de är inloggade
@views.route('/', methods=['GET', 'POST'])

# Hämtar bild-länken från databasen och returnerar den som "data"
def home():
    sql = ("SELECT * from images")
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template("index.html", user=current_user, content=data)
