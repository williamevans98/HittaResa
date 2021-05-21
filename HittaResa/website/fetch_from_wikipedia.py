import wikipedia
import pymysql
from db_connection import *
import re
import pyodbc

wikipedia.set_lang("sv")

connection = pymysql.connect(host="sql11.freemysqlhosting.net",user="sql11413883",passwd="2t3rFh95M7",database="sql11413883")

# Hämta från wikipedia
def fetch_from_wikipedia(title):
    page = wikipedia.page(title=title)
    return page

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Hämta alla locations från databasen
sql = ("SELECT location from images")
cursor.execute(sql)
locations = cursor.fetchall()

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

connection.close()






