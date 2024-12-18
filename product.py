import cv2
import apriltag

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize the AprilTag detector
detector = apriltag.Detector()


while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect AprilTags
    tags = detector.detect(gray)

    # Draw detected tags
    for tag in tags:
        corners = tag.corners
        corners = corners.astype(int)

        # Draw a rectangle around the tag
        cv2.polylines(frame, [corners], True, (0, 255, 0), 2)

        # Put tag ID text
        tag_id_text = f"ID: {tag.tag_id}"
        cv2.putText(frame, tag_id_text, tuple(corners[0]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the result
    cv2.imshow("AprilTag Detector", frame)

    # Break loop on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()