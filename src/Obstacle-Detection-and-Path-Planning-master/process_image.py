import cv2
import numpy as np
import time
import astarsearch



#Traversing through the image to perform image processing
def sliding_window(image, stepSize, windowSize):
	# slide a window across the image
	for y in range(0, image.shape[0], stepSize):
		for x in range(0, image.shape[1], stepSize):
			# yield the current window
			yield (x, y, image[y:y + windowSize[1], x:x + windowSize[0]])


def main(source , dest, cap, grid_size,frame_width, frame_height,decision):

	occupied_grids = []		# List to store coordinates of occupied grid 
	planned_path = {}		# Dictionary to store information regarding path planning  	


	_,image = cap.read()

	image = cv2.resize(image , (frame_width, frame_height))
	# load the image and define the window width and height
	(winW, winH) = (grid_size, grid_size)		# Size of individual cropped images 

	obstacles = []			# List to store obstacles (black tiles)  
	index = [1,1]
	blank_image = np.zeros((grid_size,grid_size,3), np.uint8)
	list_images = [[blank_image for i in range(frame_height//grid_size)] for i in range(frame_width//grid_size)] 	#array of list of images 
	maze = [[0 for i in range(frame_height//grid_size)] for i in range(frame_width//grid_size)] 			#matrix to represent the grids of individual cropped images

	kernel_open  = np.ones((2,2))
	kernel_close = np.ones((5,5))
	
	yellow_lower = np.array([20, 45, 27])
	yellow_upper = np.array([30, 255, 255])

	for (x, y, window) in sliding_window(image, stepSize=grid_size, windowSize=(winW, winH)):
		# if the window does not meet our desired window size, ignore it
		if window.shape[0] != winH or window.shape[1] != winW:
			continue

		clone = image.copy()
		cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
		crop_img = image[x:x + winW, y:y + winH] 				#crop the image
		list_images[index[0]-1][index[1]-1] = crop_img.copy()		

		

		img = window
		
		ctl = img
	

		hsv = cv2.cvtColor(ctl, cv2.COLOR_BGR2HSV)

		mask0 = cv2.inRange(hsv, yellow_lower, yellow_upper)

		mask = mask0

		mask_op = cv2.morphologyEx(mask , cv2.MORPH_OPEN, kernel_open)

		mask_cl = cv2.morphologyEx(mask_op, cv2.MORPH_CLOSE, kernel_close)

		Z = mask_cl.reshape((-1,1))

		Z = np.float32(Z)

		n_colors = 2

		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1)

		flags = cv2.KMEANS_RANDOM_CENTERS

		_, labels, palette = cv2.kmeans(Z, n_colors, None, criteria, 10, flags)

		_, counts = np.unique(labels, return_counts=True)

		dominant = palette[np.argmax(counts)]

		center = np.uint8(palette)

		res = center[labels.flatten()]

		res2 = res.reshape((mask_cl.shape))

		# cv2.imshow('res2',res2)


		print('decision' + str(decision))
		if decision==1:
			flag = 0
			# print(palette)
			for i in palette:
				if i[0]>=250:
					# print(i)
					if (flag==0):
						maze[index[1]-1][index[0]-1] = 1		
						cv2.rectangle(image, (x, y),(x + winW, y + winH), (255, 0, 0),-1)		
						occupied_grids.append(tuple(index))	
						flag = 1
				
			cv2.putText(clone,str(maze[index[1]-1][index[0]-1]),(x, y),
				cv2.FONT_HERSHEY_SIMPLEX ,1
				,(255,0,0),2, cv2.LINE_AA)

		cv2.imshow("window", clone)
		cv2.waitKey(1)
	
		#Iterate
		index[1] = index[1] + 1							
		if(index[1]>(frame_width//grid_size)):
			index[0] = index[0] + 1
			index[1] = 1
	
	# Apply astar algorithm on the give maze image 
	res = [[maze[j][i] for j in range(len(maze))] for i in range(len(maze[0]))]
	result = astarsearch.astar(res,(source[0],source[1]),(dest[0],dest[1]), frame_width//grid_size, frame_height//grid_size)
	
	list2=[]

	for t in result:
		x,y = t[0],t[1]
		list2.append(tuple((x+1,y+1)))			#Contains min path + startimage + endimage
	result = list(list2[1:-1]) 			#Result contains the minimum path required 

	key = cv2.waitKey(1)

	if key==27:
		cv2.destroyAllWindows()
		cap.release()

	return occupied_grids, list2



if __name__ == '__main__':

    # change filename to check for other images
    image_filename = "test_images/test_image3.jpg"

    main(image_filename)

    cv2.waitKey(0)
    
