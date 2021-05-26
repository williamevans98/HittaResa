from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from . import db
import pymysql
from db_connection import *


# Definierar views som blueprints för att vi ska kunna använda det som templates.
views = Blueprint('views', __name__)

# Routar hem när de är inloggade.
@views.route('/', methods=['GET', 'POST'])  
def home():
    '''
    Hämtar bild-länken från databasen och returnerar den som "data".
    '''
    # Skapar en connection till databasen.
    connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)
    # Förbereder ett "cursor" objekt genom att använda cursor() metoden.
    cursor = connection.cursor()
    string = str(current_user)
    get_last_element = string.split(' ')[-1]
    get_user_id = get_last_element.strip('>')
    sql = ("SELECT * FROM images WHERE NOT EXISTS (SELECT * FROM status WHERE status.image_id = images.image_id AND status.user_id = " + get_user_id + " AND status.like_or_not = 1) ORDER BY rand()")
    cursor.execute(sql)
    data = cursor.fetchall()
    connection.close()
    return render_template("index.html", user=current_user, content=data)