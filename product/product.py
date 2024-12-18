from flask import Flask, render_template, Response
import cv2
import apriltag

app = Flask(__name__)

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize the AprilTag detector
detector = apriltag.Detector()

# Frame generator
def generate_frames():
    while True:
        # Capture frame from webcam
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect AprilTags
        tags = detector.detect(gray)

        # Draw detected tags
        for tag in tags:
            corners = tag.corners.astype(int)

            # Draw a rectangle around the tag
            cv2.polylines(frame, [corners], True, (0, 255, 0), 2)

            # Put tag ID text
            tag_id_text = f"ID: {tag.tag_id}"
            cv2.putText(frame, tag_id_text, tuple(corners[0]),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Encode frame as JPEG
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