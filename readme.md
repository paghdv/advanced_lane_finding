## Advanced Lane Finding Project

The steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/undistorted.png "Undistorted"
[image2]: ./test_images/straight_lines1.jpg "Road Transformed"
[image3]: ./output_images/threshold.png "Binary Example"
[image4]: ./output_images/warped.png "Warp Example"
[image5]: ./output_images/fit_lines.png "Fit Visual"
[image6]: ./output_images/lanes.png "Output"
[video1]: ./project_video_out.mp4 "Video"


### Writeup / README

### Camera Calibration

The code for estimating the camera calibration matrix and distortion parameters is contained in the `calibrate_camera.py` file.

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result: 

![alt text][image1]

From the original image

![alt text][image2]

The calibration file is stored as a pickle file so it can be loaded later to undistor images;

### Pipeline

The pipeline can be found in the `main.py` file in the repository where the calls to the main functions are made. The global pipeline can be described in five steps.

#### 1. Undistorting images

Image undistortion is performed by loading the calibration files obtained by running `calibrate_camera.py`. The intrinsics camera matric along with the distortion parameters are loaded and used in the opencv function `undistort` to produce undistorted images. An example was just shwon above.

#### 2. Color transform gradients and thresholds.

I used a combination of color and gradient thresholds to generate a binary image. The code can be found in the file named `threshold_image.py`. Here's an example of my output for this step.

![alt text][image3]

#### 3. Perspective transform.

The code for my perspective transform estimation can be found in the function `get_perspective_transform` in `main.py` where I setup a set of correspondences between 4 points in a flat road and 4 points in a rectangle. In put the four point correspondences into the opencv function `getPerspectiveTransform` and we obtain a transfomration matrix that we can use to warp images to a top view. Note that this is only valid for flat roads.

The following is an example of the previously thresholded image now warped to a top view.

![alt text][image4]

#### 4. Identifying lane lines

In order to identify lines in the thresholded images I evaluate local histograms accross the images to identify the presence of lines. I keep the two peaks for every horizontal slice and then the lines can be made by fitting a second degree polynomial to the centers of the detected bins. The code for this section can be found in the file `find_lines.py`
We can see an example in the following image.

![alt text][image5]

#### 5. Calculating the radius of curvature of the lane and the position of the vehicle with respect to center.

I use the samples in the lane lines to obtain the radius of both curves and the overal radius is obtained by averaging both sides of the lanes. 

### Example output

To obtain the output I use the `polyfit` function from opencv to paint the lane in a warped image and then warped back to the current view by using the inverse perspective transform. An example of the result can be seen in the following image:

![alt text][image6]

A video can be seen in the following link:
<a href="http://www.youtube.com/watch?feature=player_embedded&v=T2tCscbl6y4
" target="_blank"><img src="http://img.youtube.com/vi/T2tCscbl6y4/0.jpg" 
alt="Self driving car" width="1280" height="720" border="1" /></a> 

---

### To-do

#### 1. Thresholding and line finding
The thresholding step should be further improved to remain more robust to shadows and presence of other lines. More constraints ca be added such as lane width boundaries to bias the lane finding.

#### 2. Temportal consistency
Temporal consistency could play a major role in this project since the lane finding can be stabilized by narrowing the search region to places where the lane was recently seen. Furthermore, a model could be built to take into account the motion of the car and the predicted locaiton.
