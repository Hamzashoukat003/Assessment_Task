import argparse
import csv
from datetime import datetime
import mysql.connector

class ReportGenerator:
    def __init__(self, host, user, password, database):
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.conn.cursor()

    def generate_reports(self, output_dir):
        students = self.get_students()

        self.generate_csv_report(students, output_dir)
        self.generate_html_report(students, output_dir)

        self.parse_and_insert_data(students)

    def get_students(self):
        query = """
            SELECT
                student_id,
                first_name,
                last_name,
                pin,
                date_of_birth
            FROM
                students
        """

        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        students = []
        for row in rows:
            student_id, first_name, last_name, pin, date_of_birth = row
            students.append({
                'student_id': student_id,
                'first_name': first_name,
                'last_name': last_name,
                'pin': pin,
                'date_of_birth': date_of_birth
            })

        return students

    def generate_csv_report(self, students, output_dir):
        filename = f"{output_dir}/report.csv"
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['Student ID', 'First Name', 'Last Name', 'PIN', 'Date of Birth']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for student in students:
                writer.writerow(student)

    def generate_html_report(self, students, output_dir):
        filename = f"{output_dir}/report.html"
        with open(filename, 'w') as htmlfile:
            htmlfile.write("<html><body>")
            htmlfile.write("<table border='1'><tr><th>Student ID</th><th>First Name</th><th>Last Name</th><th>PIN</th><th>Date of Birth</th></tr>")
            for student in students:
                htmlfile.write(f"<tr><td>{student['student_id']}</td><td>{student['first_name']}</td><td>{student['last_name']}</td><td>{student['pin']}</td><td>{student['date_of_birth']}</td></tr>")
            htmlfile.write("</table>")
            htmlfile.write("</body></html>")

    def parse_and_insert_data(self, students):
        for student in students:
            # Example: Parsing data and inserting it back into the database
            parsed_data = {
                'modified_first_name': student['first_name'].upper(),
                'modified_last_name': student['last_name'].lower()
            }

            update_query = """
                UPDATE students
                SET first_name = %s, last_name = %s
                WHERE student_id = %s
            """

            self.cursor.execute(update_query, (parsed_data['modified_first_name'], parsed_data['modified_last_name'], student['student_id']))

        self.conn.commit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate reports')
    args = parser.parse_args()

    generator = ReportGenerator(host='127.0.0.1', user='root', password='', database='coursera')
