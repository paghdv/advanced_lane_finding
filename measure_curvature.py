import numpy as np
import matplotlib.pyplot as plt

def measure_curvature(ploty,leftx,rightx,im_width):


#	mid = len(leftx)/2
#	leftx = np.array([leftx[0],leftx[mid],leftx[-1]])
#	rightx =np.array([rightx[0],rightx[mid],rightx[-1]])
#	ploty = np.array([ploty[0],ploty[mid],ploty[-1]]) 

	# Define conversions in x and y from pixels space to meters
	ym_per_pix = 30.0/720.0 # meters per pixel in y dimension
	xm_per_pix = 3.7/700.0 # meters per pixel in x dimension

	# Fit new polynomials to x,y in world space
	#print(np.shape(ploty*ym_per_pix))
	#print(np.shape(ploty*ym_per_pix))
	
	left_fit  = np.polyfit(ploty*ym_per_pix, leftx*xm_per_pix, 2)
	right_fit = np.polyfit(ploty*ym_per_pix, rightx*xm_per_pix, 2)

	# Plot up the data
	if False:
		mark_size = 3
		plt.plot(leftx, ploty, 'o', color='red', markersize=mark_size)
		plt.plot(rightx, ploty, 'o', color='blue', markersize=mark_size)
		plt.xlim(0, 1280)
		plt.ylim(0, 720)
		plt.plot(left_fitx, ploty, color='green', linewidth=3)
		plt.plot(right_fitx, ploty, color='green', linewidth=3)
		plt.gca().invert_yaxis() # to visualize as we do the images

	# Define y-value where we want radius of curvature
	# I'll choose the maximum y-value, corresponding to the bottom of the image
	y_eval = np.max(ploty)
	left_curverad = ((1 + (2*left_fit[0]*y_eval + left_fit[1])**2)**1.5) / np.absolute(2*left_fit[0])
	right_curverad = ((1 + (2*right_fit[0]*y_eval + right_fit[1])**2)**1.5) / np.absolute(2*right_fit[0])

	x_location=((leftx[-1]+rightx[-1])/2.0 - im_width/2.0)*xm_per_pix;

	return (left_curverad, right_curverad,x_location)
	
