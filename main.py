import cv2
from threshold_image import threshold_image
from find_lines import find_lane
from draw_output import draw_output
from measure_curvature import measure_curvature
import pickle
import numpy as np

def process_image(img,mtx,dist,M,Minv,save_steps=False):

	#undistort
	dst = cv2.undistort(img, mtx, dist, None, mtx)
	if save_steps:
		cv2.imwrite("output_images/undistorted.png",dst)
	#threshold
	dst = threshold_image(dst)
	if (save_steps):
		cv2.imwrite("output_images/threshold.png",dst)
	#rectify
	dst=cv2.warpPerspective(dst,M, (dst.shape[1],dst.shape[0]))*255#, flags=cv2.INTER_LINEAR)
	if (save_steps):
		cv2.imwrite("output_images/warped.png",dst)
	#detect lines
	(left_fitx,right_fitx,ploty)=find_lane(dst)	
	#paint image
	res=draw_output(img,M,Minv,left_fitx,right_fitx,ploty)
	if (save_steps):
		cv2.imwrite("output_images/lanes.png",res)

	#compute the curvature
	left_curverad, right_curverad, x_location=measure_curvature(ploty,left_fitx,right_fitx,img.shape[1])
	#Write info in image
	cv2.putText(res,'Turning radius: {:.6}'.format(str((left_curverad+right_curverad)/2)) + ' [deg]',(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
	cv2.putText(res,'Camera pos (x): {:.6}'.format(str(x_location)) + ' [m]',(10,70), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)

	return (res,left_curverad, right_curverad,x_location);
def get_perspective_transform():
	src=np.float32([
	 [207, 720],
	 [1100, 720],
	 [667, 440],    
	 [611, 440]

	])
	dst = np.float32([
	 [207, 720],
	 [1100, 720],
	 [1100, 110],    
	 [207,  110]
	])

	M = cv2.getPerspectiveTransform(src, dst)
	Minv = cv2.getPerspectiveTransform(dst,src)
	return (M,Minv)

#load calibration
dist_pickle = pickle.load( open( "calibration.p", "rb" ) )
mtx = dist_pickle["mtx"]
dist = dist_pickle["dist"]
#set perspective transform
(M,Minv) = get_perspective_transform()

#read sample image
img = cv2.imread("test_images/straight_lines1.jpg")
#cv2.imshow("Original",img)
#cv2.waitKey()
(res,curv_left,curv_right,x_location)=process_image(img,mtx,dist,M,Minv,True)
print ("Curvature: %f , %f",curv_left,curv_right)
cv2.imshow("Lane finding",res)
cv2.waitKey()

