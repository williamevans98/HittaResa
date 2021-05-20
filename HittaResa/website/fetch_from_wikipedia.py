import wikipedia
import pymysql
from db_connection import *
import re
import mariadb

wikipedia.set_lang("sv")

# Hämta från wikipedia
def fetch_from_wikipedia(title):
    page = wikipedia.page(title=title)
    return page

import pyodbc as db

# Öppnar anslutningen till databasen.
<<<<<<< Updated upstream
connection = pymysql.connect(host="appelgren.one.mysql", user="appelgren_onehittaresa", passwd="InformationsArkitekt2020", database="appelgren_onehittaresa")

=======
server = 'localhost'
username = 'TestUser'
password = 'a'
database = 'HittaResa'
connection = db.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' +
                        database + ';UID=' + username + ';PWD=' + password)
>>>>>>> Stashed changes

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Hämta alla locations från databasen
sql = ("SELECT location from images")
cursor.execute(sql)
locations = cursor.fetchall()
connection.close()

# Hämta wikipediasidan för alla locations
# Spara summary i en dictionary med location som key och summary som value
# Spara url i en dictionary med location som key och summary som value
summaries = {}
urls = {}
print("Fetching from wikipedia..")
for loc in locations:
    location = loc[0]

    page = fetch_from_wikipedia(location)

    # Ta ut de två första meningarna från summaryn med hjälp av regular expression (re)
    summary = ' '.join(re.split(r'(?<=[.])\s', page.summary)[:2])

    # Hämta url från wikipediasidan
    url = page.url

    urls[location] = url
    summaries[location] = summary






