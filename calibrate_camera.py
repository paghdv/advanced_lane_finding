import numpy as np
import cv2
import glob
import pickle
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('camera_cal/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(5)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
#newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,gray.shape[::-1],1,gray.shape[::-1])
img = cv2.imread('camera_cal/calibration1.jpg')
undist = cv2.undistort(img, mtx, dist, None, mtx)
#undist = cv2.undistort(img, mtx, dist, None, newcameramtx)
#x,y,w,h = roi
#print("roi %d %d %d %d %d\n",x,y,w,h)
#undist = undist[y:y+h, x:x+w]
cv2.imwrite('output_images/calibresult.png',undist)

# Save camera calibration
calib_pickle = {}
calib_pickle["mtx"] = mtx
calib_pickle["dist"] = dist
pickle.dump( calib_pickle, open( "calibration.p", "wb" ) )

#dist_pickle = pickle.load( open( "camera_cal/720x540_cal_pickle.p", "rb" ) )
#mtx = dist_pickle["mtx"]
#dist = dist_pickle["dist"]
