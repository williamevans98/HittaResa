from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db

import pyodbc as db

server = 'localhost'
username = 'TestUser'
password = 'a'
database = 'HittaResa'
connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' +
                        database + ';UID=' + username + ';PWD=' + password)
cursor = connection.cursor() # type db.Cursor

# Import av funktioner som vi använder

views = Blueprint('views', __name__)

# Definierar views som blueprints för att vi ska kunna använda det som templates

@views.route('/', methods=['GET', 'POST'])

# Routar hem när de är inloggade
#@login_required - referens för framtiden kring loginreq
def home():
    cursor.execute("SELECT * from images")
    res = cursor.fetchall()
    for item in res:
        url = item[1] 

    return render_template("index.html", user=current_user, content=url, r=2)
    
# Routar hem när de har skapat konto samt loggar in användaren