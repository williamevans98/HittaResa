import pymysql

# Öppnar anslutningen till databasen.
connection = pymysql.connect(host="sql11.freemysqlhosting.net", user="sql11405569", passwd="8M3yX3fj8V", database="sql11405569")

# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor()

# Använd denna när man lägger till nya bilder.
# Ange hela url och ange rätt namn på resmålet.
insert1 = "INSERT INTO images (location, url) values('Venedig', 'static/images/destinationsbilder-test/1.jpg');"

# Exekverar frågan som görs till databasen.
cursor.execute(insert1)

# Commitar anslutningen för att sedan stänga den.
connection.commit()
connection.close()