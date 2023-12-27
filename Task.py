# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 14:26:30 2023

@author: HAMZA SHOUKAT
"""
import csv
from datetime import datetime
import mysql.connector
import argparse
import os

class BenefitReportGenerator:
    def __init__(self, database_config, output_path, min_total_credit, date_range, pin_list=None, output_format=None):
        self.database_config = database_config
        self.output_path = output_path
        self.min_total_credit = min_total_credit
        self.date_range = date_range
        self.pin_list = pin_list
        self.output_format = output_format or ['html', 'csv']

    def connect_to_database(self):
        return mysql.connector.connect(**self.database_config)

    def generate_report(self):
        students_data = self.get_students_data()

        for student_data in students_data:
            student_name, total_credit = student_data['name'], student_data['total_credit']
            courses_data = self.get_courses_data(student_data['id'])
            
            if total_credit > self.min_total_credit:
                self.save_reports(student_name, total_credit, courses_data)

    def get_students_data(self):
        connection = self.connect_to_database()
        cursor = connection.cursor(dictionary=True)

        query = f"SELECT s.id, s.name, SUM(c.credit) AS total_credit " \
                f"FROM Students s " \
                f"LEFT JOIN Courses c ON s.id = c.student_id " \
                f"WHERE c.status = 'completed' AND c.date_completed BETWEEN %s AND %s " \
                f"GROUP BY s.id, s.name"
        
        if self.pin_list:
            query += f" HAVING s.id IN ({', '.join(['%s'] * len(self.pin_list))})"
        
        params = (self.date_range[0], self.date_range[1]) + tuple(self.pin_list) if self.pin_list else (self.date_range[0], self.date_range[1])

        cursor.execute(query, params)
        students_data = cursor.fetchall()
        cursor.close()
        connection.close()
        return students_data

    def get_courses_data(self, student_id):
        connection = self.connect_to_database()
        cursor = connection.cursor(dictionary=True)

        query = f"SELECT course_name, total_time, credit, instructor_name " \
                f"FROM Courses " \
                f"WHERE student_id = {student_id} AND status = 'completed' " \
                f"AND date_completed BETWEEN %s AND %s"
        
        cursor.execute(query, (self.date_range[0], self.date_range[1]))

        courses_data = cursor.fetchall()
        cursor.close()
        connection.close()
        return courses_data

    def save_reports(self, student_name, total_credit, courses_data):
        for format_type in self.output_format:
            if format_type == 'html':
                self.save_to_html(student_name, total_credit, courses_data)
            elif format_type == 'csv':
                self.save_to_csv(student_name, total_credit, courses_data)

    def save_to_html(self, student_name, total_credit, courses_data):
        html_content = f"<h1>{student_name}, Total Credit: {total_credit}</h1>\n"
        for course in courses_data:
            html_content += f"<p>{course['course_name']}, {course['total_time']}, {course['credit']}, {course['instructor_name']}</p>\n"

        output_file_path = os.path.join(self.output_path, f"report_{student_name}.html")
        with open(output_file_path, 'w') as html_file:
            html_file.write(html_content)

    def save_to_csv(self, student_name, total_credit, courses_data):
        csv_file_path = os.path.join(self.output_path, f"report_{student_name}.csv")
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Course Name", "Total Time", "Credit", "Instructor Name"])
            for course in courses_data:
                csv_writer.writerow([course['course_name'], course['total_time'], course['credit'], course['instructor_name']])

def parse_command_line_args():
    parser = argparse.ArgumentParser(description="Generate benefit reports for students.")
    parser.add_argument("--pin", type=str, help="Comma separated list of personal identifiers (PIN) of the students")
    parser.add_argument("--first_name", type=str, required=True, help="Output path for the reports")
    parser.add_argument("--last_name", type=int, required=True, help="Required minimum credit")
    parser.add_argument("--datetime", type=str, required=True, help="Start date of the time period (YYYY-MM-DD)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_command_line_args()
    pin_list = args.pins.split(',') if args.pins else None
    date_range = (datetime.strptime(args.start_date, '%Y-%m-%d'), datetime.strptime(args.end_date, '%Y-%m-%d'))

    db_config = {
        'host': '127.0.0.1',
        'user': 'root',
        'password': '',
        'database': 'coursera'
    }

    report_generator = BenefitReportGenerator(
        database_config=db_config,
        output_path=args.output_path,
        min_total_credit=args.min_credit,
        date_range=date_range,
        pin_list=pin_list,
        output_format=args.output_format
    )

    report_generator.generate_report()
