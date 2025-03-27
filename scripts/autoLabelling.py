import os
import cv2
from ultralytics import YOLO

# Prompt the user for input paths
model_path = "G:/My Drive/SUDISA/dev/runs/detect/train2/weights/best.pt"
video_path = input("Enter the path to the video file: ")  # Path to the input video

# Extract video name without extension
video_name = os.path.splitext(os.path.basename(video_path))[0]

# Define output folders
# output_folder = os.path.join(os.path.dirname(video_path), "output")
output_folder = "D:/SUDISA/recordings_output"
images_folder = os.path.join(output_folder, "images")  # Folder for frames
labels_folder = os.path.join(output_folder, "labels")  # Folder for labels
annotated_video_path = os.path.join(output_folder, f"{video_name}_annotated.mp4")  # Annotated video file

# Create output folders if they don't exist
os.makedirs(images_folder, exist_ok=True)
os.makedirs(labels_folder, exist_ok=True)

# Load YOLO model
model = YOLO(model_path)

# Get the class names
class_names = model.names  # A list of class names
print("Class Names: ", class_names)

# Open video file
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Error: Unable to open video file {video_path}")
    exit()

# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Prepare video writer for annotated video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(annotated_video_path, fourcc, fps, (frame_width, frame_height))

frame_index = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break  # Exit if no frame is read

    frame_index += 1
    print(f"Processing frame {frame_index}/{frame_count}...")

    # Perform detection on the current frame
    results = model(frame)

    # Frame and label filenames
    frame_filename = f"{video_name}_{frame_index - 1}.jpg"
    label_filename = f"{video_name}_{frame_index - 1}.txt"

    # Save the frame to the images folder
    frame_path = os.path.join(images_folder, frame_filename)
    cv2.imwrite(frame_path, frame)

    # Save label file in YOLO format
    label_path = os.path.join(labels_folder, label_filename)
    with open(label_path, "w") as f:
        for detection in results[0].boxes:  # Iterate through detections
            cls = int(detection.cls)  # Class ID
            conf = detection.conf.item()  # Confidence
            xywhn = detection.xywhn.tolist()[0]  # YOLO format: normalized x_center, y_center, width, height
            x_center, y_center, width, height = xywhn

            # Write label in YOLO format: class x_center y_center width height
            f.write(f"{cls} {x_center} {y_center} {width} {height}\n")

    # Annotate frame
    for detection in results[0].boxes:  # Iterate through detections
        cls = int(detection.cls)  # Class ID
        conf = detection.conf.item()  # Confidence
        xyxy = detection.xyxy.tolist()[0]  # Convert to top-left, bottom-right format

        # Draw bounding box
        x1, y1, x2, y2 = map(int, xyxy)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Add label text (class name and confidence)
        class_name = class_names[cls] if cls < len(class_names) else f"Class {cls}"
        label = f"{class_name} ({conf:.2f})"
        cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    # Save annotated frame to output video
    out.write(frame)

    # # Display the frame in real-time
    # cv2.imshow("Inference", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit early
        break

print(f"Annotated video saved: {annotated_video_path}")
print(f"Images saved in: {images_folder}")
print(f"Labels saved in: {labels_folder}")

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
