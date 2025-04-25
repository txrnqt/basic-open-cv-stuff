import cv2;
import numpy as np

#algae detection constants
ALGAE_LOWER_HSV = np.array([00, 00, 00])
ALGAE_HIGHER_HSV = np.array([00, 00, 00])
ALGAE_MINIMUM_CONTURE = 0.0
ALGAE_CONTURE_THRESHOLD = 0.0



def find_algae_colored_conture(hsv_image: np.ndarray) -> np.ndarray:
    mask = cv2.inRange(hsv_image, ALGAE_LOWER_HSV, ALGAE_HIGHER_HSV)
    
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
    capture = cv2.VideoCapture(0)
    # capture.set(3, 640)
    # capture.set(4, 480)

    while True:
        ret, frame= capture.read()
        if not ret:
            print("no cam idiot")
            break
        
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        conture = find_algae_colored_conture(frame_hsv)
        if conture is not None and conture_is_algae(conture):
            cv2.ellipse(frame, cv2.fitEllipse(conture), (255, 0, 255), 2)

        
        cv2.imshow('Webcam', frame)
        if cv2.waitKey(1) == ord('q'):
            break
    
    capture.release()
    cv2.destroyAllWindows() 
    
if __name__ == "__main__":
    main()