from IPython import display
display.clear_output()

import ultralytics
ultralytics.checks()

import cv2
import supervision as sv
from ultralytics import YOLO

model = YOLO(r"D:\SUDISA\others\model\Iter3.1n.pt")

import os
folder_path = r"D:\SUDISA\scripts\newFolder"

for id, file in enumerate(os.listdir(folder_path)):
    if file.endswith('.jpg'):
        image = cv2.imread(os.path.join(folder_path, file))
        results = model(image)[0]
        # print(f"Results: {results}")
        detections = sv.Detections.from_ultralytics(results)

        box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        annotated_image = box_annotator.annotate(
            scene=image, detections=detections)
        annotated_image = label_annotator.annotate(
            scene=annotated_image, detections=detections)

        cv2.imwrite(f"result_{id}.jpg", annotated_image)