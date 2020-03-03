import process_image
import cv2
import smooth
import numpy as np
import imutils
from collections import deque
import time


position = []
def draw_circle(event , x, y, flags, param):
    global position
    if event == cv2.EVENT_LBUTTONDBLCLK:
        position.append((x, y))


cap1 = cv2.VideoCapture(0)



cv2.namedWindow('window1')
cv2.setMouseCallback('window1' , draw_circle)


while True:

    _, frame1 = cap1.read()

    frame1 = cv2.resize(frame1,(640, 640))
    if len(position):
        for i in range(len(position)):
            source = (position[i][0], position[i][1])
            cv2.circle(frame1,source, 10, (255, 0, 0), -1)

    cv2.imshow('window1', frame1)

    key = cv2.waitKey(2)

    if key == 27:
        break  



cap1.release()
cv2.destroyAllWindows()

source = []
dest = []
if len(position)==2:
    source =  (position[0][0]/64, position[0][1]/64)
    dest = (position[1][0]/64 , position[1][1]/64)

occupied_grids, planned_path = process_image.main(source , dest)



print("Planned Path :", planned_path)
print("actual coordinates")

path = []

for x, y in planned_path:
    path.append((x*64, y*64))

print(path)

frame = np.zeros((640,640,3),np.uint8)

print("printing the command for the car")
command = list()


for x in range(len(planned_path)-1) :
    i, j = planned_path[x]
    p, q = planned_path[x+1]

    if p==i+1:
        command.append('L')
    if p==i-1:
        command.append('R')
    if q==j+1:
        command.append('F')
    if q==j-1:
        command.append('B')

print(command)                                        

qt = list()

for x in range(len(planned_path)):
    i , j = planned_path[x]
    qt.append((i , j))



cap = cv2.VideoCapture(0)
pts = np.array(path , np.int32)

color_l  = np.array([110, 50, 50])
color_h = np.array([130, 255, 255])

index = 0 # index of the list qt

# for choosing the source and destination on the given frame

while True:

    _, frame = cap.read()

    frame = cv2.resize(frame,(640, 640))

    new_frame= cv2.polylines(frame, [pts] , False, (255,120,255), 3)
    cv2.imshow('window', new_frame)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # we are only allowing the given color range in the hsv model 
    kernel = np.ones((6,6), np.uint8)

    mask = cv2.inRange(hsv , color_l , color_h)
    
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.morphologyEx(mask , cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    red_mask = cv2.bitwise_and(frame, frame, mask = mask)
    cnts,_= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
    center = None

    cX = 0
    cY = 0

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
        if radius > 5:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)


    # these coordinates coorsponds to the current position of the car 
    xt = cX/64
    yt = cY/64      

    if index!=len(qt):

        tempx, tempy = qt[index]

        if xt==tempx+1:
            print('L')
        if xt==tempx-1:
            print('R')
        if yt==tempy+1:
            print('F')
        if yt==tempy-1:
            print('B')

        if xt == tempx and yt==tempy:
            print(xt, yt)
            index+=1


    if len(position):
        for i in range(len(position)):
            source = (position[i][0], position[i][1])
            cv2.circle(frame,source, 10, (255, 0, 0), -1)
        
    cv2.imshow('window', frame)

    k = cv2.waitKey(2) & 0xFF
    
    if k == 27:
        break 

cap.release()
cv2.destroyAllWindows()
