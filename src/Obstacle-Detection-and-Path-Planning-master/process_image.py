import cv2
import numpy as np
import time
import astarsearch
import traversal
from sklearn.cluster import KMeans
from skimage import io
import matplotlib.pyplot as plt

def main(source , dest, cap, grid_size,frame_width, frame_height,decision):

	occupied_grids = []		# List to store coordinates of occupied grid 
	planned_path = {}		# Dictionary to store information regarding path planning  	
	# print('aewfoineoif')
	# cap = cv2.VideoCapture(0)

	# image = cv2.imread(im)

	_,image = cap.read()

	image = cv2.resize(image , (frame_width, frame_height))
	# load the image and define the window width and height
	# image = cv2.imread(frame)
	(winW, winH) = (grid_size, grid_size)		# Size of individual cropped images 

	obstacles = []			# List to store obstacles (black tiles)  
	index = [1,1]
	blank_image = np.zeros((grid_size,grid_size,3), np.uint8)
	list_images = [[blank_image for i in range(frame_height//grid_size)] for i in range(frame_width//grid_size)] 	#array of list of images 
	maze = [[0 for i in range(frame_height//grid_size)] for i in range(frame_width//grid_size)] 			#matrix to represent the grids of individual cropped images

	for (x, y, window) in traversal.sliding_window(image, stepSize=grid_size, windowSize=(winW, winH)):
		# if the window does not meet our desired window size, ignore it
		if window.shape[0] != winH or window.shape[1] != winW:
			continue

	#	print index
		clone = image.copy()
		cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
		crop_img = image[x:x + winW, y:y + winH] 				#crop the image
		list_images[index[0]-1][index[1]-1] = crop_img.copy()		

		

		img = window

		cv2.imshow("second_window",img)
	

		# dominant color concept to find the dominant color in each windoew
		pixels = np.float32(img.reshape(-1, 3))

		# nuber of dominant color to find inside the window
		n_colors = 3
		criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 200, .1)
		flags = cv2.KMEANS_RANDOM_CENTERS

		_, labels, palette = cv2.kmeans(pixels, n_colors, None, criteria, 10, flags)
		_, counts = np.unique(labels, return_counts=True)
		dominant = palette[np.argmax(counts)]
		# print('palette', palette)
		# print(dominant)


		# this is used to print the dominant color inside the window
		# indices = np.argsort(counts)[::-1]   
		# freqs = np.cumsum(np.hstack([[0], counts[indices]/counts.sum()]))
		# rows = np.int_(img.shape[0]*freqs)
		# dom_patch = np.zeros(shape=img.shape, dtype=np.uint8)
		# for i in range(len(rows) - 1):
		# 	dom_patch[rows[i]:rows[i + 1], :, :] += np.uint8(palette[indices[i]])

		# cv2.namedWindow('dominant',cv2.WINDOW_NORMAL)
		# cv2.resizeWindow('dominant', 600,600)
		# cv2.imshow("dominant", dom_patch)
		
		# plt.show()	

		# average color concept to find the average color in each window
		# average_color_per_row = np.average(img, axis=0)
		# average_color = np.average(average_color_per_row, axis=0)
		# average_color = np.uint8(average_color)					#Average color of the grids
		
		# print(average_color)
		
		#to identify which color we need to find 
		# print(average_color)

		#this is used for is there is black color in domianace

		# if (all(i<=50 for i in dominant)):			
		# 	maze[index[1]-1][index[0]-1] = 1				
		# 	occupied_grids.append(tuple(index))	

		# this is used for is there any black in the window 
		print('decision' + str(decision))
		if decision == 1:
			flag = 0
			for i in palette:
<<<<<<< HEAD
				if (all(j<=30 for j in i)):
=======
				if (all(j<=20 for j in i)):
>>>>>>> 62e6c82f809e06d16e6d99b45edf36e70a090d7c
					# print(i)
					if (flag==0):
						maze[index[1]-1][index[0]-1] = 1		
						cv2.rectangle(image, (x, y),(x + winW, y + winH), (0, 255, 0),2)		
						# cv2.rectangle(clone, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
						occupied_grids.append(tuple(index))	
						flag = 1
			
			cv2.putText(clone,str(maze[index[1]-1][index[0]-1]),(x, y),
				cv2.FONT_HERSHEY_SIMPLEX ,1
				,(255,0,0),2, cv2.LINE_AA)

		# cv2.imshow("hist", hist)
		# cv2.imshow("bar", bar)
		cv2.imshow("display_Window", clone)
		cv2.waitKey(1)
		# time.sleep(0.01)
	
		#Iterate
		index[1] = index[1] + 1							
		if(index[1]>(frame_width//grid_size)):
			index[0] = index[0] + 1
			index[1] = 1
	
	# Apply astar algorithm on the give maze image 
	res = [[maze[j][i] for j in range(len(maze))] for i in range(len(maze[0]))]
	result = astarsearch.astar(res,(source[0],source[1]),(dest[0],dest[1]), frame_width//grid_size, frame_height//grid_size)
	
	# printing the maze for checking
	# for i in range(len(maze)):
	# 	for j in range(len(maze[0])):
	# 		print(res[i][j],end=" ")
	# 	print(" ")	
	
	list2=[]
	# print(result)
	for t in result:
		x,y = t[0],t[1]
		list2.append(tuple((x+1,y+1)))			#Contains min path + startimage + endimage
	result = list(list2[1:-1]) 			#Result contains the minimum path required 

	# print(maze)
	# cv2.destroyAllWindows()
	# cap.release()
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
    
