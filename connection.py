import sqlite3

# Establish a connection to your database
conn = sqlite3.connect('coursera.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Ask the user for input - PINs (if any)
pins_input = input("Enter student PINs separated by commas (e.g., 111-11-111,222-22-222): ")
# Split the input into a tuple of PINs
pins = tuple(pins_input.split(',')) if pins_input else None

# Ask the user to input the minimum credit
minimum_credit = input("Enter minimum credit: ")

# Ask the user for input - start_date and end_date
start_date = input("Enter start date (YYYY-MM-DD): ")
end_date = input("Enter end date (YYYY-MM-DD): ")

# Base query to retrieve the desired information with string concatenation
query = """
SELECT
    s.first_name || ' ' || s.last_name AS student_name,
    SUM(cr.credit) AS total_credit,
    cr.name AS course_name,
    cr.total_time AS total_time,
    cr.credit AS course_credit,
    i.first_name || ' ' || i.last_name AS instructor_name
FROM
    students_courses_xref sc
JOIN
    students s ON sc.student_pin = s.pin
JOIN
    courses cr ON sc.course_id = cr.id
JOIN
    instructors i ON cr.instructor_id = i.id
"""

# Additional parameters to store user input for filtering
params = []

# Adding conditions for PINs if provided
if pins:
    query += "WHERE sc.student_pin IN ({}) ".format(','.join(['?'] * len(pins)))
    params.extend(pins)
    if start_date or end_date:
        query += "AND "
else:
    query += "WHERE " if start_date or end_date else ""

# Adding conditions for start_date and end_date
if start_date and end_date:
    query += "sc.completion_date BETWEEN ? AND ?"
    params.extend([start_date, end_date])
elif start_date:
    query += "sc.completion_date >= ?"
    params.append(start_date)
elif end_date:
    query += "sc.completion_date <= ?"
    params.append(end_date)

# Grouping and ordering of results
query += " GROUP BY student_name, course_name"

# Adding condition for minimum_credit
if minimum_credit:
    query += " HAVING total_credit >= ?"
    params.append(minimum_credit)

query += " ORDER BY student_name, course_name"

# Execute the query with parameters
cursor.execute(query, params)

# Fetch the results
results = cursor.fetchall()

# Display or process the results
for row in results:
    student_name, total_credit, course_name, total_time, course_credit, instructor_name = row
    print(f"{student_name}, {total_credit}")
    print(f"{course_name}, {total_time}, {course_credit}, {instructor_name}")

# # Display or process the results
# current_student = None
# total_student_credit = 0

# for row in results:
#     student_name, total_credit, course_name, total_time, course_credit, instructor_name = row
    
#     if current_student != student_name:
#         if current_student:
#             print(f"{current_student}, {total_student_credit}")
#         current_student = student_name
#         total_student_credit = 0
#         print(f"{current_student}, {total_credit}")
    
#     print(f"{course_name}, {total_time}, {course_credit}, {instructor_name}")
#     total_student_credit += course_credit

# # Print the last student's total credit
# if current_student:
#     print(f"{current_student}, {total_student_credit}")

# Close the connection
conn.close()
