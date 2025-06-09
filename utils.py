import os
import cv2
import numpy as np
from datetime import datetime
import sqlite3

def init_db():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    # Create students table
    c.execute('''CREATE TABLE IF NOT EXISTS students
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  image_path TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Create attendance table
    c.execute('''CREATE TABLE IF NOT EXISTS attendance
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  student_id INTEGER,
                  date DATE,
                  time TIME,
                  FOREIGN KEY (student_id) REFERENCES students(id),
                  UNIQUE(student_id, date))''')
    
    conn.commit()
    conn.close()

def insert_student(name, image_path):
    """Insert a new student into the database"""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    c.execute("INSERT INTO students (name, image_path) VALUES (?, ?)",
             (name, image_path))
    
    student_id = c.lastrowid
    conn.commit()
    conn.close()
    return student_id

def mark_attendance(student_id):
    """Mark attendance for a student"""
    try:
        conn = sqlite3.connect('attendance.db')
        c = conn.cursor()
        
        current_date = datetime.now().date()
        current_time = datetime.now().time()
        
        c.execute("INSERT INTO attendance (student_id, date, time) VALUES (?, ?, ?)",
                 (student_id, current_date, current_time))
        
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:  # Attendance already marked for today
        return False

def get_all_students():
    """Get all registered students"""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    c.execute("SELECT id, name, image_path FROM students")
    students = c.fetchall()
    
    conn.close()
    return students

def get_attendance_report(date=None):
    """Get attendance report for a specific date or all dates"""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    if date:
        c.execute("""
            SELECT s.name, a.date, a.time
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            WHERE a.date = ?
            ORDER BY a.time
        """, (date,))
    else:
        c.execute("""
            SELECT s.name, a.date, a.time
            FROM attendance a
            JOIN students s ON a.student_id = s.id
            ORDER BY a.date, a.time
        """)
    
    attendance = c.fetchall()
    conn.close()
    return attendance

def load_encodings():
    """Load all student face encodings from the database"""
    conn = sqlite3.connect('attendance.db')
    c = conn.cursor()
    
    c.execute("SELECT id, face_encoding FROM students")
    rows = c.fetchall()
    
    encodings = {}
    for student_id, encoding_bytes in rows:
        encoding = np.frombuffer(encoding_bytes, dtype=np.float64)
        encodings[student_id] = encoding
    
    conn.close()
    return encodings 