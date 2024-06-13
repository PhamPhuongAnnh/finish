from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO("best.pt")

# Run inference on 'bus.jpg' with arguments
model.predict("bien-so-vang-la-gi.jpg", save=True, imgsz=320, conf=0.5)