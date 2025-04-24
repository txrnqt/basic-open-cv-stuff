from ultralytics import YOLO

model = YOLO("yolo-Weights/yolov8n.pt")    
results = model.train(date='data.yaml', epochs=50, imgsz=640, batch=16)
print(results.metritcs)
