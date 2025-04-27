import cv2
import numpy as np
import glob

chestboardSize = (0,0)
frameSize = (1440,1080)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chestboardSize[0] * chestboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chestboardSize[0], 0:chestboardSize[1].T.reshape(-1,2)]

objPoints = []
imgPoints = []

images = glob.glob('*.png')

for images in images:
    print(image)
    img = cv2.imread(images)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, corners = cv2.findChessboardCorners(gray, chestboardSize, None)
    
    if ret == True:
        objPoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgPoints.append(corners)
        
        cv2.drawChessboardCorners(img, chestboardSize, corners2, ret)
        cv2.imshow('img', img)
        cv2.waitKey(1000)
        
cv2.destroyAllWindows()

#real calibration

ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, frameSize, None, None)

print("Camera Calibrated:", ret)
print("camera Matrix: \n", cameraMatrix)
print("Distortion Pram: \n", dist)
print("Rotation Vectors: \n", rvecs)
print("Translation Vectors: \n", tvecs)

#rm destortion

img = cv2.imread('cali5.png')
h, w = img.shape[:2]
newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))

dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('caliResult1.png')

mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv2.imwrite('caliResult2.png')

mean_error = 0
for i in range(len(objPoints)):
    imgPoints2, _ = cv2.projectPoints(objPoints[1], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv2.norm(imgPoints[1], imgPoints2, cv2.NORM_L2)/len(imgPoints2)
    mean_error += error
print("total error: {}".format(mean_error/len(objPoints)))