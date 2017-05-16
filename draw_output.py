import numpy as np
import cv2

def draw_output(img,M,Minv,left_fitx,right_fitx,ploty):
		
	# Recast the x and y points into usable format for cv2.fillPoly()
	pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
	pts_right = np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
	pts = np.hstack((pts_left, pts_right))
    
	# Create an image to draw the lines on
	lane_img = np.zeros_like(img).astype(np.uint8)

    # Draw the lane onto the warped blank image
	cv2.fillPoly(lane_img, np.int_([pts]), (0,255, 0))
	cv2.polylines(lane_img, np.array([pts_left], dtype=np.int32), False,(255,0,0),thickness = 15)
	cv2.polylines(lane_img, np.array([pts_right], dtype=np.int32), False,(0,0,255),thickness = 15)

	# Warp the blank back to original image space using inverse perspective matrix (Minv)
	lane_warped = cv2.warpPerspective(lane_img, Minv, (img.shape[1], img.shape[0])) 
	# Combine the result with the original image
	result = cv2.addWeighted(img, 1, lane_warped, 0.3, 0)
	return result
