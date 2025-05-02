import numpy as np
import cv2 as cv
import glob

CHECKERBOARD = (9,7)
critera = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objPoints = []
imgPoints = []

objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

images = glob.glob('calibration/*.jpg')
for read in images:
    # print(read)
    img = cv.imread(read)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # print(gray)
    ret, corners = cv.findChessboardCorners(gray, CHECKERBOARD, cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_FAST_CHECK + cv.CALIB_CB_NORMALIZE_IMAGE)
    
    if ret == True:
        objPoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), critera)
        imgPoints.append(corners2)
        
        img = cv.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
    print(objPoints)
    print(imgPoints)
cv.destroyAllWindows()
# print(gray)
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None) 
print("Camera matrix : \n")
print(mtx)
print("dist : \n")
print(dist)
print("rvecs : \n")
print(rvecs)
print("tvecs : \n")
print(tvecs)