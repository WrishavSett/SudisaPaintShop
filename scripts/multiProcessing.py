import cv2
from ultralytics import YOLO

# Load a pretrained YOLO model
model = YOLO("yolo11n.pt")
model.fuse()
model.half()

def read_video():
    source = cv2.VideoCapture(0)
    if not source.isOpened():
        print("Error: Could not access video source. Exiting.")
        exit()
    return source

def process_frame(frame):
    results = model(frame, conf=0.75)
    return results

def handle_output(results, frame):
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
            conf = box.conf[0]  # Confidence score
            cls = box.cls[0]  # Class ID
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            label = f"{model.names[int(cls)]} {conf:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
    return frame

def show(frame):
    cv2.imshow("YOLO Real-Time Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False
    return True

def main():
    source = read_video()
    while True:
        ret, frame = source.read()
        if not ret:
            print("Error: Unable to read video frame. Exiting.")
            break

        # Process the frame
        results = process_frame(frame)

        # Handle output and draw bounding boxes
        frame = handle_output(results, frame)

        # Show the output frame
        if not show(frame):
            break

    # Release resources
    source.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()