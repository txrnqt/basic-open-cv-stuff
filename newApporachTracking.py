import cv2
import numpy as np
import imutils
import math

#algae constants

GREEN_LOWER = np.ndarray((30, 100, 50)) #est
GREEN_UPPER = np.ndarray((85, 255, 255)) #est
BALL_DIAMITER = 0.406 #in meters

#camera constants
FOCAL_LENGTH = 0 #TODO
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

#camera to robot
CAMERA_HEIGHT = 0.0 #meters TODO
CAMERA_ANGLE = 0.0 #radians TODO
CENTER_X = FRAME_WIDTH / 2
CENTER_Y = FRAME_HEIGHT / 2

class pose2D: 
    x: float
    y: float
    theata: float

while True:
    ret, frame = cam.read()
    if not ret:
        print("no cam")
        break
    
    #image cleaning
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    
    #threshold for green mask
    mask = cv2.inRange(hsv, GREEN_LOWER, GREEN_UPPER)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    if cnts:
        c = max(cnts, key=cv2.contourArea)
        ((cx, cy), radius_px) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] > 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"]/M["m00"]))
        else:
            center = (int(cx), int(cy))
        
        
        #x robot forward, y robot right
        if radius_px > 10:
            distance = (BALL_DIAMITER * FOCAL_LENGTH) / (2.0 * radius_px)
            dx = (cx - CENTER_X)
            bearing = math.atan2(dx, FOCAL_LENGTH)
            X = distance * math.cos(bearing)
            Y = distance * math.sin(bearing)
            theta = bearing
            
            #adjust x with camera tilt and height
            target_pose = pose2D(x=X, y=Y, theta=theta)
            
            cv2.circle(frame, (int(cx), int(cy)), int(radius_px), (0,255,0), 2)
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) == ord('q'):
                break
        else:
            pass
    else:
        pass
cam.release()
cv2.destroyAllWindows()