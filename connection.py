# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:58:11 2023

@author: HAMZA SHOUKAT
"""


# import required modules 
import mysql.connector

# create connection object
con = mysql.connector.connect(
    host="localhost", user="root",
    password="", database="coursera"
)

# create cursor object
cursor = con.cursor()

# execute query to get list of tables
query_tables = "SHOW TABLES"
cursor.execute(query_tables)

# display all tables
tables = cursor.fetchall()
print('\nTables in the database:')
for table in tables:
    print(table[0])

# specify the table you want to describe
table_to_describe = "courses"

# describe table
query_describe = f"DESCRIBE {table_to_describe}"
cursor.execute(query_describe)

# display table description
print(f'\nTable Description for {table_to_describe}:')
for attr in cursor.fetchall():
    print(attr)

# execute query to get data from students table
query_students = "SELECT * FROM students"
cursor.execute(query_students)

# display all records from the students table
table_students = cursor.fetchall()
print('\nTable Data for students:')
for row in table_students:
    print(row[0], row[1], row[2], row[3])

# closing cursor connection
cursor.close()

# closing connection object
con.close()
