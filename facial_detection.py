import cv2
import face_recognition
import os

# Load reference images
current_dir = os.path.dirname(os.path.abspath(__file__))
reference_images = {
    "You": os.path.join(current_dir, "reference_images", "fynn.jpg"),
    "Friend": os.path.join(current_dir, "reference_images", "flo.jpg")
}

# Verify images exist
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

        # Use the first matching face
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

    # Display result
    cv2.imshow("Webcam Footage", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()