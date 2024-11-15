import mysql.connector

from secrets_1 import USER, PASSWORD

# Establish connection to the MySQL server 
connection = mysql.connector.connect(
    host='127.0.0.1',
    user=USER,
    password=PASSWORD,
    database='SWT'
)


