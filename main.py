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
		cv2.imwrite("output_images/threshold.png",dst*255)
	#rectify
	dst=cv2.warpPerspective(dst,M, (dst.shape[1],dst.shape[0]))*255#, flags=cv2.INTER_LINEAR)
	if (save_steps):
		cv2.imwrite("output_images/warped.png",dst)
	#detect lines
	(left_fitx,right_fitx,ploty,bins)=find_lane(dst)	
	if (save_steps):
		cv2.imwrite("output_images/fit_lines.png",bins)
	#paint image
	res=draw_output(img,M,Minv,left_fitx,right_fitx,ploty)
	if (save_steps):
		cv2.imwrite("output_images/lanes.png",res)

	#compute the curvature
	left_curverad, right_curverad, x_location=measure_curvature(ploty,left_fitx,right_fitx,img.shape[1])
	#Write info in image
	cv2.putText(res,'Turning radius: {:.6}'.format(str((left_curverad+right_curverad)/2)) + ' [m]',(10,30), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2)
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

def process_video(file_in,file_out,resolution):
	#running the videos
	cap_in  = cv2.VideoCapture(file_in)
	cap_out = cv2.VideoWriter(file_out, cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 20.0, resolution)
	k=0;
	while(cap_in.isOpened()):
		ret, frame = cap_in.read()
		if ret:
			(res,curv_left,curv_right,x_location)=process_image(frame,mtx,dist,M,Minv,False)
		    # write frame
			cap_out.write(res)
		else:
		    break
		k=k+1;
		print(k)
	# Release everything if job is finished
	cap_in.release()
	cap_out.release()

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
(res,curv_left,curv_right,x_location) = process_image(img,mtx,dist,M,Minv,True)
print ("Curvature: %f , %f",curv_left,curv_right)
cv2.imshow("Lane finding",res)
cv2.waitKey()

#process_video("challenge_video.mp4", "challenge_video_out.mp4",(1280,720))
#process_video("project_video.mp4", "project_video_out.mp4",(1280,720))
