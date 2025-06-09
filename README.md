# Face Recognition Attendance System

A Python-based attendance system that uses facial recognition to mark student attendance automatically. The system includes a web interface for viewing and managing attendance records.

## Features

- Student registration with face detection
- Real-time face recognition for attendance marking
- Web interface for viewing attendance records
- Filter attendance by date
- Export attendance records to CSV
- View registered students list
- Prevents duplicate attendance entries for the same day

## Prerequisites

- Python 3.7 or higher
- Webcam
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd face-recognition-attendance
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Register Students:
```bash
python register.py
```
- Enter the student's name when prompted
- Press SPACE to capture the photo when ready
- Press ESC to exit registration

2. Start Attendance System:
```bash
python recognize.py
```
- The system will automatically detect faces and mark attendance
- Press 'q' to quit

3. View Attendance Records (Web Interface):
```bash
python app.py
```
- Open a web browser and go to http://localhost:5000
- View attendance records and registered students
- Filter attendance by date
- Export attendance records to CSV

## Project Structure

```
face_attendance/
├── dataset/                 # Registered student face images
├── templates/              # HTML templates for web interface
├── attendance.db           # SQLite database
├── app.py                 # Flask web application
├── recognize.py           # Face recognition script
├── register.py            # Student registration script
├── utils.py               # Helper functions
└── requirements.txt       # Python dependencies
```

## Notes

- The system uses face_recognition library which is based on dlib
- Make sure there is good lighting when registering faces and marking attendance
- Only one face should be visible during registration
- The system prevents duplicate attendance entries for the same day
- Attendance records are stored in a SQLite database

## Contributing

Feel free to submit issues and enhancement requests! 