import sqlite3

# Connect to a database (it will be created if it doesn't exist)
conn = sqlite3.connect('coursera.db')
cursor = conn.cursor()

# Create the students table
cursor.execute('''
    CREATE TABLE students (
        pin NCHAR(10) NOT NULL UNIQUE,
        first_name NVARCHAR(50) NOT NULL,
        last_name NVARCHAR(50) NOT NULL,
        time_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create the instructors table
cursor.execute('''
    CREATE TABLE instructors (
        id INTEGER PRIMARY KEY NOT NULL,
        first_name NVARCHAR(100) NOT NULL,
        last_name NVARCHAR(100) NOT NULL,
        time_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
''')

# Create the courses table
cursor.execute('''
    CREATE TABLE courses (
        id INTEGER PRIMARY KEY NOT NULL,
        name NVARCHAR(150) NOT NULL,
        instructor_id INTEGER NOT NULL,
        total_time TINYINT NOT NULL,
        credit TINYINT NOT NULL,
        time_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (instructor_id) REFERENCES instructors(id)
    )
''')

# Create the students_courses_xref table
cursor.execute('''
    CREATE TABLE students_courses_xref (
        student_pin NCHAR(10) NOT NULL,
        course_id INTEGER NOT NULL,
        completion_date DATE DEFAULT CURRENT_DATE,
        FOREIGN KEY (student_pin) REFERENCES students(pin),
        FOREIGN KEY (course_id) REFERENCES courses(id)
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()