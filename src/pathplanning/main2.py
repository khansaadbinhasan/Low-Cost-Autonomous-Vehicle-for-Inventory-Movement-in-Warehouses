import process_image
import cv2
import smooth
import numpy as np
import imutils
from collections import deque
import time
import socket
import math
import traversal
import rst


width_box = 0
height_box = 0
def distance(x1 , y1 , x2 , y2): 
  
    # Calculating distance 
    return math.sqrt(math.pow(x2 - x1, 2) +
                math.pow(y2 - y1, 2) * 1.0)

def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    width_box = w
    height_box = h
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3 )
    cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)


STOP = '0'
UP = '1'
DOWN = '2'
RIGHT = '3'
LEFT = '4'

SEND_COMMAND = STOP


# # Setting up TCP connection
TCP_IP = '192.168.43.208' # IP of raspberry pi
TCP_PORT = 5005

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((TCP_IP, TCP_PORT))


# default size of the grid and the frame
grid_size = 64
frame_height= 640
frame_width= 640


print('enter the grid size')
grid_size = int(input())
print('enter the frame_height')
frame_height = int(input())
print('enter the frame_width')
frame_width = int(input())
print('With object detection or not--> 0= NO and 1= YES')
decision = int(input())



position = []
def draw_circle(event , x, y, flags, param):
    global position
    if event == cv2.EVENT_LBUTTONDBLCLK:
        position.append((x, y))


index = 0 # index of the list qt
 # center = None
cX = 0
cY = 0

# estinmated coornates
x_est = 0
y_est = 0


m_x, m_y = 0,0
val = 0

tempx = 0
tempy = 0

# destination of the path to reach 
# final_x, final_y = qt[-1]

(winW, winH) = (grid_size, grid_size)


def next_point(img, qt, xt, yt):

        # assume evchicle did not stop at any of the subgoal
        global tempx, tempy, index, grid_size

        if distance(tempx, tempy ,xt, yt)<grid_size:
            print('next point')
            index+=1

        if index == len(qt):
            return -1,-1
        
        tempx, tempy = qt[index]
        tempx = tempx*grid_size
        tempy = tempy*grid_size

        # cv2.circle(img,(int(x_est), int(y_est)), 2, (0, 255, 0), 5)
        # cv2.putText(img, str(int(x_est)) + " "+ str(int(y_est)), (int(x_est), int(y_est)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,255 ), 2)

        cv2.circle(img,(int(tempx), int(tempy)), 10, (0, 255, 0), 5)
        cv2.circle(img,(int(tempx), int(tempy)), 15, (0, 255, 0), 5)
        cv2.putText(img, str(int(tempx)) + " "+ str(int(tempy)), (int(tempx), int(tempy)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,255 ), 2)

        return tempx, tempy


cap1 = cv2.VideoCapture(0)



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
            # cv2.putText(frame1,str(position[i][0]) + " " 
            #     +str(position[i][1]), (position[i][0], position[i][1]),
            #      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)


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

cap = cv2.VideoCapture(0)

occupied_grids, planned_path= process_image.main(source , dest,cap,grid_size, frame_width, frame_height,decision)



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

# colors that need to adjusted

o1 = [93,168,22] # green sticker
o2 = [100,255,255]
p1 = [107,120,16] # blue sticker
p2 = [130,255,255]

while True:

    # for drawing the matrix on to the frame
    _, img = cap.read()
    img = cv2.resize(img,(frame_width, frame_height))

    x1, y1, ret1 = rst.get_moments(img, o1, o2, 1)
    x2, y2, ret2 = rst.get_moments(img, p1, p2, 2)

    cv2.imshow('Orange',ret1)
    cv2.imshow('Pink',ret2)

    xt = (x1+x2)//2
    yt = (y1 +y2)//2

    cv2.circle(img,(int(xt), int(yt)), 2, (0, 255, 0), 5)

    next_x, next_y = next_point(img, qt, xt, yt)
    if (next_x == -1 and next_y == -1):
        print("destination Reached")
        break



    # if distance(xt, yt ,final_x, final_y)<grid_size:
    #     print("destination Reached")

    car_angle=rst.get_direction(x1, y1, x2, y2)
    actual_angle = rst.get_direction(xt, yt, tempx, tempy)

    result=rst.path_encode(car_angle, actual_angle)

    print(result)

    img = cv2.line(img,(x1, y1),(x2, y2), (0,255,0), 3)
    img = cv2.line(img, (xt, yt),(next_x, next_y),(0,0,255), 3)


    SEND_COMMAND = result
    direction= ""
    if SEND_COMMAND=='0':
        direction  = "Stop"
    if SEND_COMMAND =='1':
        direction = "up"
    if SEND_COMMAND =='2':
        direction = "down"
    if SEND_COMMAND =='3':
        direction = "right"
    if SEND_COMMAND =='4':
        direction = "left"

    print('Action ' + direction)
    flag = 0
    # s.send(str(SEND_COMMAND))

    if len(path):
        for i in range(len(path)):
            source = (path[i][0], path[i][1])
            if i==0 or i==len(path)-1:
                cv2.circle(img,source, 2, (255, 0, 0), 10)
            else:
                cv2.circle(img,source, 2, (255, 0, 0), 2)      
             

    
    cv2.imshow('window', img)

    time.sleep(0.05)
    k = cv2.waitKey(2) & 0xFF
    
    if k == 27:
        break 


# SEND_COMMAND = STOP
# s.send(str(SEND_COMMAND))
# s.close()
cap.release()
cv2.destroyAllWindows()