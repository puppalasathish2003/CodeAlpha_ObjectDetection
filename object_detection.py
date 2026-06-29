import cv2
import time
import os
from ultralytics import YOLO

# -----------------------------
# Create screenshots folder
# -----------------------------
os.makedirs("screenshots", exist_ok=True)

# -----------------------------
# Load YOLOv8 Model
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# Open Webcam
# -----------------------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access webcam.")
    exit()

prev_time = 0
image_count = 1

print("=" * 50)
print("AI Object Detection Started")
print("Press 'S' to save screenshot")
print("Press 'Q' to Quit")
print("=" * 50)

# -----------------------------
# Main Loop
# -----------------------------
while True:

    success, frame = cap.read()

    if not success:
        break

    # Detect objects
    results = model(frame, verbose=False)

    annotated_frame = results[0].plot()

    # -----------------------------
    # FPS Calculation
    # -----------------------------
    current_time = time.time()
    fps = 1 / (current_time - prev_time) if prev_time != 0 else 0
    prev_time = current_time

    cv2.putText(
        annotated_frame,
        f"FPS : {int(fps)}",
        (15, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        "Press S : Save Screenshot",
        (15, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 0),
        2
    )

    cv2.putText(
        annotated_frame,
        "Press Q : Quit",
        (15, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),
        2
    )

    cv2.imshow("CodeAlpha AI Object Detection", annotated_frame)

    key = cv2.waitKey(1)

    # -----------------------------
    # Save Screenshot
    # -----------------------------
    if key == ord('s') or key == ord('S'):

        filename = f"screenshots/detection_{image_count}.jpg"

        cv2.imwrite(filename, annotated_frame)

        print(f"Screenshot Saved : {filename}")

        image_count += 1

    # -----------------------------
    # Exit
    # -----------------------------
    if key == ord('q') or key == ord('Q'):
        break

# -----------------------------
# Cleanup
# -----------------------------
cap.release()
cv2.destroyAllWindows()

print("\nObject Detection Closed Successfully!")