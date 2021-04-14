import pymysql

# Open database connection
connection = pymysql.connect(host="sql11.freemysqlhosting.net", user="sql11405569", passwd="8M3yX3fj8V", database="sql11405569")
# prepare a cursor object using cursor() method
cursor = connection.cursor()

# Använd denna när man lägger till nya bilder.
# Ange hela url och ange rätt namn på resmålet
insert1 = "INSERT INTO user (email, username, password) values('test@gmail.com', 'admin', 'password');"

#executing the quires
cursor.execute(insert1)

#commiting the connection then closing it.
connection.commit()
connection.close()