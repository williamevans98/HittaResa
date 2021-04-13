# Import av funktioner som vi använder
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
import pyodbc as db

# Ansluter till databasen
server = 'localhost'
username = 'TestUser'
password = 'a'
database = 'HittaResa'
connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' +
                        database + ';UID=' + username + ';PWD=' + password)
cursor = connection.cursor() # type db.Cursor

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


# En snabb liten funktion som kan lägga till en ny bild-länk i databasen. Kallas ej på någonstans än!
# Exempel-länk till bild: static/images/destinationsbilder-test/1.jpg
def add_image_URL():
    print("Funkar endast med .jpg format")
    print("Behöver inte ange länk och format, ange endast filnamn")
    filnamn = input("Ange filnamn: ")
    URL = "static/images/destinationsbilder-test/" + filnamn + ".jpg"
    cursor.execute("INSERT into images (url) VALUES (?)", URL)
    connection.commit()
    print(URL + " Har lags till i databasen")