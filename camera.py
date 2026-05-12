import cv2
import numpy as np

# Open Camera
camera = cv2.VideoCapture(0)

# Check camera
if not camera.isOpened():
    print("Camera not detected")
    exit()

print("Smart Surveillance Camera Started")

while True:

    # Read Frame
    ret, frame = camera.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Convert to HSV for color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red Color Range
    lower_red = np.array([0, 120, 70])
    upper_red = np.array([10, 255, 255])

    # Detect Red Color
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detected_color = "No Color Detected"

    for contour in contours:

        area = cv2.contourArea(contour)

        if area > 1000:

            x, y, w, h = cv2.boundingRect(contour)

            # Draw Rectangle
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 0, 255),
                2
            )

            detected_color = "Red Color Detected"

            cv2.putText(
                frame,
                detected_color,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

    # Display Status
    cv2.putText(
        frame,
        "Smart Surveillance Robot",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 255, 255),
        2
    )

    # Show Video
    cv2.imshow("Surveillance Camera", frame)

    # Press Q to Exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release Camera
camera.release()

# Close Windows
cv2.destroyAllWindows()
