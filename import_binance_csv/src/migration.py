import csv
import sys
import mysql.connector
from operator import delitem
from mysql.connector import errorcode
from decouple import config

# Check if the filename was provided
if (len(sys.argv) < 2):
    print("Filename was not provided!")
    exit()

print('Get the filename to import')
filename = sys.argv[1]
 
# initializing the titles and rows list
fields = []
rows = []


try:
    cnx = mysql.connector.connect(user=config('USER'), password=config('PASSWORD'),
                                 host=config('HOST'),
                                 database='crypto-tracker')

    with open(filename, newline='\n') as csvfile:


except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cnx.close()