import os
from ultralytics import YOLO
import pandas as pd
from datetime import datetime

# Initialize YOLOv8 model (lightweight version for speed)
model = YOLO("yolov8n.pt")

# Define the directory where images are saved
base_dir = "C:/Users/user/Desktop/tasks/End_To_End_Medical_Intelligence_Platform/data/raw/images"
output_records = []

# Traverse the directory recursively
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(root, file)

            # Run detection
            results = model(img_path)

            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    label = r.names[cls_id]
                    conf = float(box.conf[0])

                    # Extract message_id from filename (e.g., "123456_image1.jpg")
                    message_id = file.split('_')[0]

                    output_records.append({
                        "message_id": message_id,
                        "image_path": img_path.replace('\\', '/'),  # Unix-style path for compatibility
                        "detected_object_class": label,
                        "confidence_score": conf,
                        "detected_at": datetime.now().isoformat()
                    })

# Save results to CSV
df = pd.DataFrame(output_records)
output_csv = "C:/Users/user/Desktop/tasks/End_To_End_Medical_Intelligence_Platform/data/raw/yolo_detections.csv"
df.to_csv(output_csv, index=False)

print(f"Detection complete. Results saved to {output_csv}")
