import process_image
import cv2
# import smooth
import numpy as np
import imutils
from collections import deque
import time
import socket


from parameters import numCam, robotHSVlow, robotHSVhigh, grid_size, frame_height, frame_width, decision 


############### Tracker Types #####################
 
#tracker = cv2.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerTLD_create()
#tracker = cv2.TrackerMedianFlow_create()
#tracker = cv2.TrackerCSRT_create()

tracker = cv2.TrackerMOSSE_create()


def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
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

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


# default size of the grid and the frame
# grid_size = 128
# frame_height= 640
# frame_width= 640
# decision = 0

# print('enter the grid size')
# grid_size = int(input())
# print('enter the frame_height')
# frame_height = int(input())
# print('enter the frame_width')
# frame_width = int(input())
# print('With object detection or not--> 0= NO and 1= YES')
# decision = input()


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

occupied_grids, planned_path = process_image.main(source , dest,cap,grid_size, frame_width, frame_height,decision)



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

# color_l  = np.array([robotHSVlow['Hue'], robotHSVlow['Sat'], robotHSVlow['Val'] ])
# color_h = np.array([robotHSVhigh['Hue'], robotHSVhigh['Sat'], robotHSVhigh['Val']])

index = 0 # index of the list qt

# for choosing the source and destination on the given frame
flag = 1


success, frame = cap.read()
frame = cv2.resize(frame,(frame_width, frame_height))
bbox = cv2.selectROI("Tracking",frame, False)
tracker.init(frame, bbox)


 # center = None
cX = 0
cY = 0

min_v = 9999999
m_x, m_y = 0,0
val = 0

tempx = 0
tempy = 0

# destination of the path to reach 
final_x, final_y = qt[-1]



while True:

    timer = cv2.getTickCount()
    success, img = cap.read()
    img = cv2.resize(img,(frame_width, frame_height))
    success, bbox = tracker.update(img)
 


    if success:
        # print(success)
        
        drawBox(img,bbox)
        x = int((bbox[0] + bbox[2])/2)
        y = int((bbox[1] + bbox[3])/2)
        cX = x
        cY = y
        cv2.putText(img,str(x) + " " +str(y), (int(bbox[0]),int(bbox[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    else:
        cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
    cv2.rectangle(img,(15,15),(200,90),(255,0,255),2)
    # cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,255), 2);
    # cv2.putText(img, "Status:", (20, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2);
 
 
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
    if fps>60: myColor = (20,230,20)
    elif fps>20: myColor = (230,20,20)
    else: myColor = (20,20,230)
    cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);
 
    img= cv2.polylines(img, [pts] , False, (255,120,255), 3)

    
    # cv2.imshow('window', img)
    


    xt = cX
    yt = cY

    if distance(xt, yt ,final_x, final_y)<grid_size:
        print("destination Reached")
        break


    if index!=len(qt):
        # assume evchicle did not stop at any of the subgoal
        if distance(tempx, tempy ,xt, yt)<grid_size:
            print('next point')
            index+=1
            min_v = 999999
        tempx, tempy = qt[index]
        tempx = tempx*grid_size
        tempy = tempy*grid_size
        x_est, y_est = xt, yt

        print(tempx, tempy)
        cv2.circle(img,(int(x_est), int(y_est)), 2, (0, 255, 0), 5)
        cv2.putText(img, str(int(x_est)) + " "+ str(int(y_est)), (int(x_est), int(y_est)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,255 ), 2)

        cv2.circle(img,(int(tempx), int(tempy)), 10, (0, 255, 0), 5)
        cv2.circle(img,(int(tempx), int(tempy)), 15, (0, 255, 0), 5)
        cv2.putText(img, str(int(tempx)) + " "+ str(int(tempy)), (int(tempx), int(tempy)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,255 ), 2)

        p1_x, p1_y = xt + 1, yt 
        p2_x, p2_y = xt - 1, yt 
        p3_x, p3_y = xt , yt +1
        p4_x, p4_y = xt , yt -1


        if distance(p1_x, p1_y, tempx, tempy) < min_v:
            min_v = distance(p1_x, p1_y, tempx, tempy)
            m_x , m_y= p1_x, p1_y
            val = RIGHT

        if distance(p2_x, p2_y, tempx, tempy) < min_v:
            min_v = distance(p2_x, p2_y, tempx, tempy)
            m_x, m_y= p2_x, p2_y
            val = LEFT
        if distance(p3_x, p3_y, tempx, tempy) < min_v:
            min_v = distance(p3_x, p3_y, tempx, tempy)
            m_x,m_y = p3_x, p3_y
            val = DOWN
        if distance(p4_x, p4_y, tempx, tempy) < min_v:
            min_v = distance(p4_x, p4_y, tempx, tempy)
            m_x, m_y = p4_x, p4_y
            val = UP

        x_est, y_est = m_x, m_y
        SEND_COMMAND = str(val)

    # to print the direcction of the car
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

    
    print(SEND_COMMAND)
    s.send(str(SEND_COMMAND).encode())

    if len(path):
        for i in range(len(path)):
            source = (path[i][0], path[i][1])
            if i==0 or i==len(path)-1:
                cv2.circle(img,source, 2, (255, 0, 0), 10)
            else:
                cv2.circle(img,source, 2, (255, 0, 0), 2) 

    # pt.appendleft(center)
                    
    # for i in range(1, len(pt)):
    #             # if either of the tracked points are None, ignore
    #             # them
    #     if pt[i - 1] is None or pt[i] is None:
    #         continue
    #             # otherwise, compute the thickness of the line and
    #             # draw the connecting lines
    #     thickness = int(np.sqrt(30 // float(i + 1)) * 2.5)
    #     cv2.line(frame, pt[i - 1], pt[i], (0, 0, 255), thickness)
             

    
    cv2.imshow('window', img)

    time.sleep(0.05)
    k = cv2.waitKey(2) & 0xFF
    
    if k == 27:
        break 


SEND_COMMAND = STOP
s.send(str(SEND_COMMAND).encode())
s.close()
cap.release()
cv2.destroyAllWindows()
