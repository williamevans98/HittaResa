import wikipedia
import pymysql
from db_connection import *
import re
import pyodbc

wikipedia.set_lang("sv")

# Skapar en connection till databasen
connection = pymysql.connect(host=database_host,user=database_user,passwd=database_password,database=database_name)

def fetch_from_wikipedia(title):
    '''
    Hämtar information från wikipedia för att sedan skriva ut rätt information på rätt location.
    '''
    page = wikipedia.page(title=title)
    return page

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Hämta alla locations från databasen.
sql = ("SELECT location from images")
cursor.execute(sql)
locations = cursor.fetchall()

# Hämtar wikipediasidan för alla locations.
# Sparar summary i en dictionary med location som key och summary som value.
# Sparar url i en dictionary med location som key och summary som value.
summaries = {}
urls = {}
print("Fetching from wikipedia..")
for loc in locations:
    location = loc[0]

    page = fetch_from_wikipedia(location)

    # Ta ut de två första meningarna från summaryn med hjälp av regular expression (re).
    summary = ' '.join(re.split(r'(?<=[.])\s', page.summary)[:2])

    # Hämta url från wikipediasidan.
    url = page.url

    urls[location] = url
    summaries[location] = ('%.150s' % summary)

connection.close()






