import math
import cv2
from ultralytics import YOLO

modle = YOLO("yolo-Weights/epoch-69.pt")

classNames = ["algae", "coral", "reef"]

capture = cv2.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

while True:
    ret, img= capture.read()
    results = modle(img, stream=True)
    
    for r in results:
        boxes = r.boxes
        
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->", confidence)
            
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])
            
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2 

            cv2.putText(img, classNames[cls], org, font, fontScale, color, thickness)
    cv2.imshow('Webcam', img)
    
    if cv2.waitKey(1) == ord('q'):
        break
    
capture.release()
cv2.destroyAllWindows() 