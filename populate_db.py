import sqlite3
from random import choice
from datetime import datetime, timedelta


# Function to generate random date within a year range from today
def random_date(start_date, end_date):
    return start_date + timedelta(seconds=choice(range(int((end_date - start_date).total_seconds()))))

# Connect to the database
conn = sqlite3.connect('coursera.db')
cursor = conn.cursor()

# Generate and insert records for students
students = [
        {
            "pin": "111-11-111",
            "first_name": "Hamza",
            "last_name": "Tariq"
        },
        {
            "pin": "222-22-222",
            "first_name": "Usama",
            "last_name": "Tariq"
        },
        {
            "pin": "333-33-333",
            "first_name": "Arslan",
            "last_name": "Munir"
        },
        {
            "pin": "444-44-444",
            "first_name": "Asad",
            "last_name": "Munir"
        },
        {
            "pin": "555-55-555",
            "first_name": "Haris",
            "last_name": "Turk"
        }
    ]
for _ in range(5):
    pin = students[_]["pin"]
    first_name = students[_]["first_name"]
    last_name = students[_]["last_name"]
    cursor.execute("INSERT INTO students (pin, first_name, last_name) VALUES (?, ?, ?)",
                   (pin, first_name, last_name))

# Generate and insert records for instructors
instructors = [
        {
            "first_name": "John",
            "last_name": "Doe"
        },
        {
            "first_name": "Jane",
            "last_name": "Doe"
        },
        {
            "first_name": "Mark",
            "last_name": "Smith"
        },
        {
            "first_name": "Sara",
            "last_name": "Smith"
        },
        {
            "first_name": "David",
            "last_name": "Brown"
        }
]
for _ in range(5):
    first_name = instructors[_]["first_name"]
    last_name = instructors[_]["last_name"]
    cursor.execute("INSERT INTO instructors (first_name, last_name) VALUES (?, ?)",
                   (first_name, last_name))

# Generate and insert records for courses
for _ in range(5):
    name = "Course " + str(_ + 1)
    instructor_id = choice(range(1, 6))  # Assuming you have 5 instructors with IDs from 1 to 5
    total_time = choice(range(25, 31))  # Assuming total_time ranges from 1 to 10
    credit = choice(range(5, 15))  # Assuming credit ranges from 1 to 5
    cursor.execute("INSERT INTO courses (name, instructor_id, total_time, credit) VALUES (?, ?, ?, ?)",
                   (name, instructor_id, total_time, credit))

# Generate and insert records for students_courses_xref
for _ in range(5):
    student_pin = students[_]["pin"]
    course_id = choice(range(1, 6))  # Assuming you have 5 courses with IDs from 1 to 5
    if _ % 2 == 0:
        completion_date = None
    else:
        completion_date = random_date(datetime.now(), datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO students_courses_xref (student_pin, course_id, completion_date) VALUES (?, ?, ?)",
                   (student_pin, course_id, completion_date))

# Commit changes and close the connection
conn.commit()
conn.close()