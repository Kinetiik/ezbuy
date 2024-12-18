from flask import Flask, render_template, Response
import cv2
import face_recognition
import os

app = Flask(__name__)

# Load reference images
current_dir = os.path.dirname(os.path.abspath(__file__))
reference_images = {
    "You": os.path.join(current_dir, "reference_images", "fynn.jpg"),
    "Friend": os.path.join(current_dir, "reference_images", "flo.jpg")
}

# Verify reference images exist
for name, path in reference_images.items():
    if not os.path.exists(path):
        print(f"Error: Missing reference image for {name}. Please place the image in {path}.")
        exit()

# Load and encode reference images
known_face_encodings = []
known_face_names = []

for name, path in reference_images.items():
    image = face_recognition.load_image_file(path)
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append(name)

# Initialize webcam
cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame for faster processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Find face locations and encodings
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings = face_recognition.face_encodings(small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]

            # Adjust scaling back to original frame size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw box around face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(host='0.0.0.0', port=port, debug=True)