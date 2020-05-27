import cv2
import imutils
from collections import deque
import numpy as np
import time
from parameters import numCam

def detection():
		cap = cv2.VideoCapture(numCam)

		color_l  = (170, 86, 6)
		color_h = (180, 255, 255)

		#width  = vcap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
		#height = vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

		# height and width of the fram is 640 * 480 need to adjust the algorithm according to that 

		# print("width ", width , "height " , height)

		pts = deque(maxlen=30)

		while True:

			_, frame = cap.read()

			# cv2.imshow("Frame", frame)

			blured_frame = cv2.GaussianBlur(frame, (5, 5) , 0)

			hsv = cv2.cvtColor(blured_frame, cv2.COLOR_BGR2HSV)
			# we are only allowing the given color range in the hsv model 
			mask = cv2.inRange(hsv , color_l , color_h)
			# mask = cv2.erode(mask, None, iterations=2)
			# mask = cv2.dilate(mask, None, iterations=2)

			red_mask = cv2.bitwise_and(frame, frame, mask = mask)

			#cv2.imshow("Frame", hsv)

			cnts,_= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
			# cv2.drawContours(frame, cnts , -1, (0,255,0), 2)
			# cnts = imutils.grab_contours(cnts)
			center = None

			
			if len(cnts) > 0:
				c = max(cnts, key=cv2.contourArea)
				((x, y), radius) = cv2.minEnclosingCircle(c)
				M = cv2.moments(c)
				if M["m00"] != 0:
		 			cX = int(M["m10"] / M["m00"])
		 			cY = int(M["m01"] / M["m00"])
				else:
		 			cX, cY = 0, 0
				center = (cX , cY)
				# only proceed if the radius meets a minimum size
				if radius > 10:
					# draw the circle and centroid on the frame,
					# then update the list of tracked points
					cv2.circle(frame, (int(x), int(y)), int(radius),
						(0, 255, 255), 2)
					cv2.circle(frame, center, 5, (0, 0, 255), -1)
			# print(cX/60, cY/60)
			'''
			pts.appendleft(center)
					
			for i in range(1, len(pts)):
				# if either of the tracked points are None, ignore
				# them
				if pts[i - 1] is None or pts[i] is None:
					continue
				# otherwise, compute the thickness of the line and
				# draw the connecting lines
				thickness = int(np.sqrt(30 / float(i + 1)) * 2.5)
				cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)		

			'''

			# cv2.imshow("Frame", frame)		

			return cX, cY

			key = cv2.waitKey(1)

			if key == ord("q"):
				break