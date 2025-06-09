from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
from datetime import datetime
from utils import get_attendance_report, get_all_students
import os

app = Flask(__name__)

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

@app.route('/')
def index():
    # Get all attendance records
    attendance_records = get_attendance_report()
    
    # Convert to pandas DataFrame for easy manipulation
    df = pd.DataFrame(attendance_records, columns=['Name', 'Date', 'Time'])
    
    # Get unique dates for the date filter
    dates = sorted(df['Date'].unique(), reverse=True)
    
    # Get filter parameters
    selected_date = request.args.get('date', '')
    
    # Apply filters
    if selected_date:
        df = df[df['Date'] == selected_date]
    
    # Convert to HTML table
    table_html = df.to_html(classes='table table-striped', index=False)
    
    return render_template('index.html', table=table_html, dates=dates, selected_date=selected_date)

@app.route('/students')
def students():
    # Get all registered students
    students_list = get_all_students()
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(students_list, columns=['ID', 'Name', 'Image Path'])
    
    # Convert to HTML table
    table_html = df.to_html(classes='table table-striped', index=False)
    
    return render_template('students.html', table=table_html)

@app.route('/export')
def export_attendance():
    # Get all attendance records
    attendance_records = get_attendance_report()
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(attendance_records, columns=['Name', 'Date', 'Time'])
    
    # Save to CSV
    csv_path = 'attendance_export.csv'
    df.to_csv(csv_path, index=False)
    
    return send_file(csv_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True) 