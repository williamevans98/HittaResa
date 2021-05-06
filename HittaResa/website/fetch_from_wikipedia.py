import wikipedia
import pymysql
from db_connection import *

wikipedia.set_lang("sv")

# Hämta från wikipedia
def fetch_from_wikipedia(title):
    summary = wikipedia.summary(title, sentences=2)
    return summary

# Öppnar anslutningen till databasen.
connection = pymysql.connect(host=database_host, user=database_user, passwd=database_password, database=database_name)

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Hämta alla locations från databasen
sql = ("SELECT location from images")
cursor.execute(sql)
locations = cursor.fetchall()
connection.close()

# Hämta summaries från wikipedia för alla locations
# Spara i en dictionary med location som key och summary som value
summaries = {}
print("Fetching from wikipedia..")
for loc in locations:
    location = loc[0]
    summary = fetch_from_wikipedia(location)
    summaries[location] = summary






