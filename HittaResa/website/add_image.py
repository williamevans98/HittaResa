import pymysql
import pyodbc as db
from db_connection import *

# Öppnar anslutningen till databasen.
connection = pymysql.connect(host=database_host,
user=database_user,passwd=database_password,database=database_name)

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor() # type db.Cursor

# Använd denna när man lägger till nya bilder.
# Ange hela url och ange rätt namn på resmålet.
#insert1 = "INSERT INTO images (location, url) values('Ystad', 'static/images/destinationsbilder-test/1.jpg');"

# Exekverar frågan som görs till databasen.
#cursor.execute(insert1)

# Commitar anslutningen för att sedan stänga den.
#connection.commit() 
connection.close()