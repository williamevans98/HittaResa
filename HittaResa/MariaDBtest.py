# Module Imports

import mariadb
import sys 

# Connect to MariaDB Platform

try: conn = mariadb.connect( 

    user="appelgren_onehittaresa", 
    password="InformationsArkitekt2020", 
    host="appelgren.one.mysql", 
    port=3306, 
    database="appelgren_onehittaresa" 
) 
except mariadb.Error as e: 
    print(f"Error connecting to MariaDB Platform: {e}") 
    sys.exit(1) 
# Get Cursor 

cur = conn.cursor()