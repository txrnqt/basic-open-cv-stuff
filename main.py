import os
import math
import ntcore
import cv2 as cv
import numpy as np
from ultralytics import YOLO


# class pose3D: 
#     def __init__(self, x, y, z, theata):
#         x: float
#         y: float
#         z: float
#         theata: float

# inst = ntcore.NetworkTableInstance.getDefault()
# table = inst.getTable("gamePeiceFind")
# algaePose = table.getFloatArrayTopic("algaePose").publish(pose3D(0.0, 0.0, 0.0, 0.0))
# isConnected = table.getIntegerTopic("isConnected").publish(1)
# inst.startClient4("gamePeiceFind")
# inst.setServerTeam(5572)

modle = YOLO("yolo-Weights/epoch-69.pt")

classNames = ["algae", "coral", "reef"]

capture = cv.VideoCapture(0)
capture.set(3, 640)
capture.set(4, 480)

def calibrate():
    root = os.getcwd()
    paramPath = os.path.join(root, 'calibration.npx')
    data = np.load(paramPath)
    camMatrix = data['camMatrix']
    distCoeff = data['distCoeff']
    rvecs = data['rvecs']
    tvecs = data['tvecs']
    cv.calibrateCamera(cameraMatrix=camMatrix, distCoeffs=distCoeff, rvecs=rvecs, tvecs=tvecs)

def findAlgae():
    ret, img= capture.read()
    results = modle(img, stream=True)
    
    for r in results:
        boxes = r.boxes
        
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            cv.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            confidence = math.ceil((box.conf[0]*100))/100
            print("Confidence --->", confidence)
            
            cls = int(box.cls[0])
            print("Class name -->", classNames[cls])
            
            org = [x1, y1]
            font = cv.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2 
            cv.putText(img, classNames[cls], org, font, fontScale, color, thickness)
        cv.imshow('Webcam', img)
capture.release()

while True:
    findAlgae()
    
    if cv.waitKey(1) == ord('q'):
        break