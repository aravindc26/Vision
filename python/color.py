from cv import *  #bad practice, its just that am bit lazy

def GetThresholdedImage(img):
#returns thresholded image of the blue bottle
	imgHSV = CreateImage(GetSize(img), 8, 3)
#converts a BGR image to HSV
	CvtColor(img, imgHSV, CV_BGR2HSV)
	imgThreshed = CreateImage(GetSize(img), 8, 1)
#InRangeS takes source, lowerbound color, upperbound color and destination
#It converts the pixel values lying within the range to 255 and stores it in
#the destination
        InRangeS(imgHSV, (100, 94, 84), (109, 171, 143), imgThreshed)
	return imgThreshed

posX = 0
posY = 0

def main():
	color_tracker_window = "output"
	thresh_window = "thresh"
	capture = CaptureFromCAM(-1)
	NamedWindow( color_tracker_window, 1 ) 
	NamedWindow( thresh_window, 1 ) 
	imgScrible = None
	global posX
	global posY
	while True:
		
		frame = QueryFrame(capture)
		Smooth(frame, frame, CV_BLUR, 3)
		
		if(imgScrible is None):
			imgScrible = CreateImage(GetSize(frame), 8, 3)
		
		imgBlueThresh = GetThresholdedImage(frame)
		
		mat = GetMat(imgBlueThresh)
#Calculating the moments
                moments = Moments(mat, 0) 
            	area = GetCentralMoment(moments, 0, 0)
		moment10 = GetSpatialMoment(moments, 1, 0)
		moment01 = GetSpatialMoment(moments, 0,1)
		
#lastX and lastY stores the previous positions
		lastX = posX
		lastY = posY
#Finding a big enough blob
		if(area > 100000): 
			
#Calculating the coordinate postition of the centroid
			posX = int(moment10 / area)
			posY = int(moment01 / area)

			print 'x: ' + str(posX) + ' y: ' + str(posY) + ' area: ' + str(area)
#drawing lines to track the movement of the blob
			if(lastX > 0 and lastY > 0 and posX > 0 and posY > 0):
				Line(imgScrible, (posX, posY), (lastX, lastY), Scalar(0, 255, 255), 5)
#Adds the three layers and stores it in the frame
#frame -> it has the camera stream
#imgScrible -> it has the line tracking the movement of the blob
			Add(frame, imgScrible, frame)

                ShowImage(thresh_window, imgBlueThresh)
		ShowImage(color_tracker_window, frame)
		c = WaitKey(10)
		if(c!=-1):
			break
		
	return;
if __name__ == "__main__":
	main()
