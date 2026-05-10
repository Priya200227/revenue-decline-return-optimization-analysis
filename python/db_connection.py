import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Priya@200227',
    database='style_union'
)

print("Database connected successfully!")
