# Import av funktioner som vi använder
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db
import pymysql

# Öppnar anslutningen till databasen.
connection = pymysql.connect(host="sql11.freemysqlhosting.net", user="sql11410449", passwd="EWSU2hrvn9", database="sql11410449")

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
    sql = ("SELECT * FROM `images` WHERE NOT EXISTS (SELECT * FROM status WHERE status.image_id = images.image_id AND status.user_id = " + get_user_id + ")")
    cursor.execute(sql)
    data = cursor.fetchall()
    return render_template("index.html", user=current_user, content=data)
    connection.close()
