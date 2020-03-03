import cv2
import numpy as np
import time
import astarsearch
import traversal



def main(source , dest):

	occupied_grids = []		# List to store coordinates of occupied grid 
	planned_path = {}		# Dictionary to store information regarding path planning  	
	# print('aewfoineoif')
	cap = cv2.VideoCapture(0)

	_,image = cap.read()

	image = cv2.resize(image , (640, 640))
	# load the image and define the window width and height
	(winW, winH) = (64, 64)		# Size of individual cropped images 

	obstacles = []			# List to store obstacles (black tiles)  
	index = [1,1]
	blank_image = np.zeros((64,64,3), np.uint8)
	list_images = [[blank_image for i in xrange(10)] for i in xrange(10)] 	#array of list of images 
	maze = [[0 for i in xrange(10)] for i in xrange(10)] 			#matrix to represent the grids of individual cropped images

	for (x, y, window) in traversal.sliding_window(image, stepSize=64, windowSize=(winW, winH)):
		# if the window does not meet our desired window size, ignore it
		if window.shape[0] != winH or window.shape[1] != winW:
			continue

	#	print index
		clone = image.copy()
		cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
		crop_img = image[x:x + winW, y:y + winH] 				#crop the image
		list_images[index[0]-1][index[1]-1] = crop_img.copy()			#Add it to the array of images

		average_color_per_row = np.average(crop_img, axis=0)
		average_color = np.average(average_color_per_row, axis=0)
		average_color = np.uint8(average_color)					#Average color of the grids
		# print (average_color)
		# the average of the grid unit is the value of the average_color 
		# in the BGR format

		# hsv=cv2.cvtColor(average_color,cv2.COLOR_BGR2HSV)

		# print(hsv)

		#to identify which color we need to find 
		if (any( i>=170 and i<=180 for i in average_color)):			
			maze[index[1]-1][index[0]-1] = 1				#ie not majorly white
			occupied_grids.append(tuple(index))				#These grids are termed as occupied_grids 

	
		cv2.imshow("Window", clone)
		cv2.waitKey(1)
		time.sleep(0.009)
	
		#Iterate
		index[1] = index[1] + 1							
		if(index[1]>10):
			index[0] = index[0] + 1
			index[1] = 1
	
	# Apply astar algorithm on the give maze image 
	result = astarsearch.astar(maze,(source[0],source[1]),(dest[0],dest[1]))
	#			print result
	list2=[]
	print(result)
	for t in result:
		x,y = t[0],t[1]
		list2.append(tuple((x+1,y+1)))			#Contains min path + startimage + endimage
	result = list(list2[1:-1]) 			#Result contains the minimum path required 

	print(maze)
	cv2.destroyAllWindows()

	return occupied_grids, list2



if __name__ == '__main__':

    # change filename to check for other images
    image_filename = "test_images/test_image3.jpg"

    main(image_filename)

    cv2.waitKey(0)
    
