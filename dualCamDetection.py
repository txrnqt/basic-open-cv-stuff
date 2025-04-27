import cv2;
import numpy as np

#camera constants
CAMERA_LEFT = 0
CL_HEIGHT = 0
CL_ANGLE = 0
CL_X = 0
CL_Y =0

CAMERA_RIGHT = 1
CR_HEIGHT = 0
CR_ANGLE = 0
CR_X = 0
CR_Y =0

#algae detection constants
GREEN_LOWER = np.array([30, 100, 50]) #est
GREEN_UPPER = np.array([85, 255, 255]) #est
BALL_DIAMETER = 0.406 #in meters
ALGAE_MINIMUM_CONTURE = 0.0
ALGAE_CONTURE_THRESHOLD = 0.0



def find_algae_colored_conture(hsv_image: np.ndarray) -> np.ndarray:
    mask = cv2.inRange(hsv_image, GREEN_LOWER, GREEN_UPPER)
    
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        return max(contours, key=cv2.contourArea)

def conture_is_algae(conture: np.ndarray) -> bool:
    if cv2.contourArea(conture) < ALGAE_MINIMUM_CONTURE:
        return False
    
    conture_hull = cv2.convexHull(conture)
    ellipse = cv2.fitEllipse(conture_hull)
    best_fit_elepise_area = np.pi * (ellipsis[1][0] / 2) * (ellipsis[1][1] / 2)
    
    return cv2.contourArea(conture_hull) / best_fit_elepise_area > ALGAE_CONTURE_THRESHOLD


def main ():
    captureLeft = cv2.VideoCapture(CAMERA_LEFT)
    captureRight = cv2.VideoCapture(CAMERA_RIGHT)


    while True:
        ret, frameLeft= captureLeft.read()
        ret, frameRight= captureRight.read()
        if not ret:
            print("no cam idiot")
            break
        
        hsvLeft = cv2.cvtColor(frameLeft, cv2.COLOR_BGR2HSV)
        hsvRight = cv2.cvtColor(frameRight, cv2.COLOR_BGR2HSV)
        
        contureLeft = find_algae_colored_conture(hsvLeft)
        contureRight = find_algae_colored_conture(hsvRight)
        
        
        if (contureLeft and contureRight) and (conture_is_algae(contureLeft) and conture_is_algae(contureRight)):
            cL = max(contureLeft, key=cv2.contourArea)
            cR = max(contureRight, key=cv2.contourArea)
            
            ((xL, yL), radiusL) = cv2.minEnclosingCircle(cL)
            ((xR, yR), radiusR) = cv2.minEnclosingCircle(cR)
            
            center_left = (int(xL), int(yL))
            center_right = (int(xR), int(yR))
            
            print(f"Left center: {center_left}, Right center: {center_right}")
        
        gray_left = cv2.cvtColor(frameLeft, cv2.COLOR_BAYER_BG2GRAY)
        gray_right = cv2.cvtColor(frameRight, cv2.COLOR_BAYER_BG2GRAY)
        
        stero = cv2.StereoSGbm
            
            
        cv2.imshow('Webcam', frameLeft)
        cv2.imshow('Webcam', frameRight)
        if cv2.waitKey(1) == ord('q'):
            break
    
    captureLeft.release()
    cv2.destroyAllWindows() 
    
if __name__ == "__main__":
    main()