import pymysql
import pyodbc as db
import mariadb

# Öppnar anslutningen till databasen.

connection = pymysql.connect(host="appelgren.one.mysql", user="appelgren_onehittaresa", passwd="InformationsArkitekt2020", database="appelgren_onehittaresa")


# Förbereder ett "cursor" objekt genom att använda cursor() metoden.
cursor = connection.cursor() # type db.Cursor

# Använd denna när man lägger till nya bilder.
# Ange hela url och ange rätt namn på resmålet.
insert1 = "INSERT INTO images (location, url) values('Ystad', 'static/images/destinationsbilder-test/1.jpg');"


#insert1 = "INSERT INTO status (user_id, image_id, like_or_not) values(26, 2, 1);"

# Exekverar frågan som görs till databasen.
cursor.execute(insert1)

# Commitar anslutningen för att sedan stänga den.
connection.commit() 





#Använd på gillar.html
#SELECT * FROM `images`
#JOIN status on images.image_id = status.image_id
#WHERE like_or_not = 1 AND user_id = 26 


#Använd denna för att visa upp alla bilder som inte har blivit gillade för en inloggad användare
#Denna måste dock kopplas till rätt användare för att visa upp rätt bilder till rätt användare (26 kommer alltså ersättas med användarens ID )
#SELECT * FROM `images` WHERE NOT EXISTS (SELECT * FROM status WHERE status.image_id = images.image_id AND status.user_id = 26)



#Använd på index för att visa upp alla bilder för en användare som inte är inloggad 
#SELECT * FROM `images` WHERE NOT EXISTS (SELECT * FROM status WHERE status.image_id = images.image_id AND status.user_id = NULL)


#index.html
    #visa (endast) de bilder som inte är gillade (NULL)
            #show * in images where like_or_not = NULL

#gillar.html
    #visa endast de bilder som är gillade (1)
        #if inloggad
            #Använd på gillar.html (ändra 26 till current_user)
            #SELECT * FROM `images`
            #JOIN status on images.image_id = status.image_id
            #WHERE like_or_not = 1 AND user_id = 26 
        #else
            #visa ett meddelande


#swipe.js
    #Ändra status på bilden
        #if bilden == gillad
            #ändra status
        #else
            #pass