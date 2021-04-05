from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from . import db

# Import av funktioner som vi använder

views = Blueprint('views', __name__)

# Definierar views som blueprints för att vi ska kunna använda det som templates

@views.route('/', methods=['GET', 'POST'])

# Routar hem när de är inloggade
#@login_required - referens för framtiden kring loginreq
def home():
    return render_template("index.html", user=current_user)

# Routar hem när de har skapat konto samt loggar in användaren