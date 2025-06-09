import cv2
import numpy as np
from datetime import datetime
from utils import get_all_students, mark_attendance
from bson import ObjectId

def recognize_faces():
    # Get all registered students
    students = get_all_students()
    
    if not students:
        print("No registered students found! Please register students first.")
        return
    
    # Load face detection classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    # For FPS calculation
    prev_time = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Process each detected face
        for (x, y, w, h) in faces:
            # Extract face region
            face_roi = frame[y:y+h, x:x+w]
            
            # Compare with registered students
            best_match = None
            best_match_score = float('inf')
            
            for student_id, name, img_path in students:
                # Load registered student image
                student_img = cv2.imread(img_path)
                if student_img is None:
                    continue
                
                # Resize to same size for comparison
                student_img = cv2.resize(student_img, (w, h))
                face_roi_resized = cv2.resize(face_roi, (w, h))
                
                # Convert to grayscale for comparison
                student_gray = cv2.cvtColor(student_img, cv2.COLOR_BGR2GRAY)
                face_roi_gray = cv2.cvtColor(face_roi_resized, cv2.COLOR_BGR2GRAY)
                
                # Calculate difference score
                diff = cv2.absdiff(student_gray, face_roi_gray)
                score = np.mean(diff)
                
                if score < best_match_score:
                    best_match_score = score
                    best_match = (student_id, name)
            
            # If good match found
            if best_match and best_match_score < 50:  # Threshold for matching
                student_id, name = best_match
                
                # Try to mark attendance
                if mark_attendance(ObjectId(student_id)):  # Convert string ID to ObjectId
                    color = (0, 255, 0)  # Green for success
                    text = f"{name} - Marked!"
                else:
                    color = (0, 255, 255)  # Yellow for already marked
                    text = f"{name} - Already Marked"
            else:
                color = (0, 0, 255)  # Red for unknown
                text = "Unknown"
            
            # Draw box around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            
            # Draw label below face
            cv2.rectangle(frame, (x, y+h-35), (x+w, y+h), color, cv2.FILLED)
            cv2.putText(frame, text, (x+6, y+h-6),
                       cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        # Calculate and display FPS
        current_time = datetime.now()
        fps = 1 / (current_time - datetime.fromtimestamp(prev_time)).total_seconds()
        prev_time = current_time.timestamp()
        cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('Face Recognition Attendance System', frame)
        
        # Break loop on 'q' press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognize_faces() 