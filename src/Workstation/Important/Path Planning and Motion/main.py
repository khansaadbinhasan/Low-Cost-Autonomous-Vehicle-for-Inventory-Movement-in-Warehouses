import process_image
import cv2
# import smooth
import numpy as np
import imutils
from collections import deque
import time
import socket
# import traversal

from parameters import numCam, STOP, UP, DOWN, RIGHT, LEFT, direction, grid_size, frame_height, frame_width, decision, TCP_IP, TCP_PORT


############### Tracker Types #####################
 
#tracker = cv2.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerTLD_create()
#tracker = cv2.TrackerMedianFlow_create()
#tracker = cv2.TrackerCSRT_create()
# tracker = cv2.TrackerMOSSE_create()

position = []



def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 3, 3 )
    cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

def distance(x1,y1,x2,y2):
    return np.sqrt((x2-x1)**2+(y2-y1)**2)

def draw_circle(event , x, y, flags, param):
    global position
    if event == cv2.EVENT_LBUTTONDBLCLK:
        position.append((x, y))

def main():
    SEND_COMMAND = STOP
    LAST_COMMAND = SEND_COMMAND


    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.connect((TCP_IP, TCP_PORT))



    # deque for movement detection
    pt = deque(maxlen=10)
    cap = cv2.VideoCapture(numCam)



    cv2.namedWindow('window')
    cv2.setMouseCallback('window' , draw_circle)

    # function to draw the source and destination
    while True:

        _, frame = cap.read()

        frame = cv2.resize(frame,(frame_width, frame_height))
        if len(position):
            for i in range(len(position)):
                source = (position[i][0], position[i][1])
                cv2.circle(frame,source, 10, (255, 0, 0), -1)

        cv2.imshow('window', frame)

        key = cv2.waitKey(2)

        if key == 27:
            break  


    source = []
    dest = []

    if len(position)==2:
        source =  (position[0][0]//grid_size, position[0][1]//grid_size)
        dest = (position[1][0]//grid_size , position[1][1]//grid_size)

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

    index = 0 # index of the list qt

    success, frame = cap.read()
    frame = cv2.resize(frame,(frame_width, frame_height))
    bbox = cv2.selectROI("window",frame, False)
    tracker.init(frame, bbox)


    cX = 0
    cY = 0

    min_v = 500
    m_x, m_y = 0,0
    val = 0

    tempx = 0
    tempy = 0

    # destination of the path to reach 
    final_x, final_y = qt[-1]

    (winW, winH) = (grid_size, grid_size)


    while True:

        timer = cv2.getTickCount()
        success, img = cap.read()
        img = cv2.resize(img,(frame_width, frame_height))
        success, bbox = tracker.update(img)
     
        if success:
            drawBox(img,bbox)
            x = int(bbox[0] + (bbox[2]/2))
            y = int(bbox[1] + (bbox[3]/2))
            cX = x
            cY = y
            cv2.putText(img,str(x) + " " +str(y), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        else:
            cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
     
        cv2.rectangle(img,(15,15),(200,90),(255,0,255),2)

        # this code is used for making grids
        for (x, y, window) in process_image.sliding_window(img, stepSize=grid_size, windowSize=(winW, winH)):
            # if the window does not meet our desired window size, ignore it
            if window.shape[0] != winH or window.shape[1] != winW:
                continue
            cv2.rectangle(img, (x, y), (x + winW, y + winH), (0, 255, 0), 2)
     
     
     
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        if fps>60: myColor = (20,230,20)
        elif fps>20: myColor = (230,20,20)
        else: myColor = (20,20,230)

        cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);
     
        img = cv2.polylines(img, [pts] , False, (255,120,255), 3)

        
        xt = cX
        yt = cY

        if distance(xt, yt ,final_x, final_y) < grid_size:
            print("destination Reached")
            break


        if index < len(qt) - 1:
            # assume evchicle did not stop at any of the subgoal
            if distance(tempx, tempy ,xt, yt)<grid_size:
                print('next point')
                index+=1
                min_v = 500

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

            dis1 = distance(p1_x, p1_y, tempx, tempy)
            dis2 = distance(p2_x, p2_y, tempx, tempy)
            dis3 = distance(p3_x, p3_y, tempx, tempy)
            dis4 = distance(p4_x, p4_y, tempx, tempy)

            if dis1 < min_v:
                min_v = dis1
                m_x , m_y= p1_x, p1_y
                val = RIGHT

            if dis2 < min_v:
                min_v = dis2
                m_x, m_y= p2_x, p2_y
                val = LEFT
            if dis3 < min_v:
                min_v = dis3
                m_x,m_y = p3_x, p3_y
                val = DOWN
            if dis4 < min_v:
                min_v = dis4
                m_x, m_y = p4_x, p4_y
                val = UP

            x_est, y_est = m_x, m_y
            SEND_COMMAND = val



        print('Action ' + direction[SEND_COMMAND])
     
        
        if LAST_COMMAND != SEND_COMMAND:
            # s.send(SEND_COMMAND.encode())
            LAST_COMMAND = SEND_COMMAND

        if len(path):
            for i in range(len(path)):
                source = (path[i][0], path[i][1])
                if i==0 or i==len(path)-1:
                    cv2.circle(img,source, 2, (255, 0, 0), 10)
                else:
                    cv2.circle(img,source, 2, (255, 0, 0), 2) 

        cv2.imshow('window', img)

        if cv2.waitKey(2) & 0xFF == 27:
            break 


    SEND_COMMAND = STOP
    print(SEND_COMMAND.encode())
    # s.send(SEND_COMMAND.encode())
    # s.close()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
