import os
import cv2
from utils import init_db, insert_student

def register_student():
    # Create dataset directory if it doesn't exist
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    
    # Initialize database
    init_db()
    
    # Get student name
    name = input("Enter student name: ")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    
    # Load face detection classifier
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw rectangle around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
        # Display the frame
        cv2.imshow('Register Student - Press SPACE to capture', frame)
        
        # Wait for spacebar press to capture image
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Spacebar
            if len(faces) == 0:
                print("No face detected! Please try again.")
                continue
                
            if len(faces) > 1:
                print("Multiple faces detected! Please try again with only one face.")
                continue
            
            # Save image
            img_path = os.path.join('dataset', f"{name}.jpg")
            cv2.imwrite(img_path, frame)
            
            # Save to database
            student_id = insert_student(name, img_path)
            print(f"Successfully registered {name} with ID {student_id}")
            break
            
        elif key == 27:  # ESC
            break
    
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    register_student() 