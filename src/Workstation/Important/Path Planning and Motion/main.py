import cv2
import numpy as np
import imutils
from collections import deque
import time
import socket


from parameters import numCam, robotHSVlow, robotHSVhigh
import process_image



STOP = '0'
UP = '1'
DOWN = '2'
RIGHT = '3'
LEFT = '4'

SEND_COMMAND = STOP


# Setting up TCP connection
TCP_IP = '192.168.43.208' # IP of raspberry pi
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


# default size of the grid and the frame
grid_size = 320
frame_height= 640
frame_width= 640


position = []
def draw_circle(event , x, y, flags, param):
    global position
    if event == cv2.EVENT_LBUTTONDBLCLK:
        position.append((x, y))


# deque for movement detection
pt = deque(maxlen=10)
cap1 = cv2.VideoCapture(numCam)



cv2.namedWindow('window1')
cv2.setMouseCallback('window1' , draw_circle)

# function to draw the source and destination
while True:

    _, frame1 = cap1.read()

    frame1 = cv2.resize(frame1,(frame_width, frame_height))
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
    source =  (position[0][0]//grid_size, position[0][1]//grid_size)
    dest = (position[1][0]//grid_size , position[1][1]//grid_size)

cap = cv2.VideoCapture(numCam)

occupied_grids, planned_path = process_image.main(source , dest,cap,grid_size, frame_width, frame_height)



print("Planned Path :", planned_path)
print("actual coordinates")

path = []

for x, y in planned_path:
    path.append((x*grid_size, y*grid_size))

print(path)

frame = np.zeros((frame_width, frame_height,3),np.uint8)

qt = list()

for x in range(len(planned_path)):
    i , j = planned_path[x]
    qt.append((i , j))




pts = np.array(path , np.int32)

color_l  = np.array([robotHSVlow['Hue'], robotHSVlow['Sat'], robotHSVlow['Val'] ])
color_h = np.array([robotHSVhigh['Hue'], robotHSVhigh['Sat'], robotHSVhigh['Val']])

index = 0 # index of the list qt

# for choosing the source and destination on the given frame
flag = 1


while True:

    _, frame = cap.read()

    frame = cv2.resize(frame,(frame_width, frame_height))

    # making the paths from source to desination 

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
            cX = int(M["m10"] // M["m00"])
            cY = int(M["m01"] // M["m00"])
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
    xt = cX/grid_size
    yt = cY/grid_size


    if index!=len(qt):

        tempx, tempy = qt[index]

        if xt==tempx+1:
            SEND_COMMAND = LEFT
        elif xt==tempx-1:
            SEND_COMMAND = RIGHT
        elif yt==tempy+1:
            SEND_COMMAND = UP
        elif yt==tempy-1:
            SEND_COMMAND = DOWN

        if xt == tempx and yt==tempy:
            flag=1
            index+=1

    # send command will be printed as the signal for the car
    if (flag ):
    	print('Action ' + SEND_COMMAND)
    	flag = 0

    
    print(SEND_COMMAND)
    s.send(str(SEND_COMMAND).encode())

    if len(position):
        for i in range(len(position)):
            source = (position[i][0], position[i][1])
            cv2.circle(frame,source, 10, (255, 0, 0), -1)

    pt.appendleft(center)
                    
    for i in range(1, len(pt)):
                # if either of the tracked points are None, ignore
                # them
        if pt[i - 1] is None or pt[i] is None:
            continue
                # otherwise, compute the thickness of the line and
                # draw the connecting lines
        thickness = int(np.sqrt(30 // float(i + 1)) * 2.5)
        cv2.line(frame, pt[i - 1], pt[i], (0, 0, 255), thickness)
             

    
    cv2.imshow('window', frame)

    time.sleep(0.05)
    k = cv2.waitKey(2) & 0xFF
    
    if k == 27:
        break 


SEND_COMMAND = STOP
s.send(str(SEND_COMMAND).encode())
s.close()
cap.release()
cv2.destroyAllWindows()