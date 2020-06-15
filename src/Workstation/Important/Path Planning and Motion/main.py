import cv2, imutils
import numpy as np
import socket
import time

import process_image
from parameters import numCam, STOP, UP, DOWN, RIGHT, LEFT, direction, grid_size, frame_height, frame_width, decision, TCP_IP_RPI, TCP_PORT_WASD, TCP_IP_WORKSTATION, TCP_PORT_IMU_DATA, BUFFER_SIZE, tracker


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

def make_connections():
    s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s1.connect((TCP_IP_RPI, TCP_PORT_WASD))


    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind((TCP_IP_WORKSTATION, TCP_PORT_IMU_DATA))
    s2.listen(1)

    conn, addr = s2.accept()
    print ('Connection address:', addr)


    return s1, conn

def draw_source_dest(cap):
    # function to draw the source and destination
    cv2.namedWindow('window')
    cv2.setMouseCallback('window' , draw_circle)


    while True:

        _, frame = cap.read()

        frame = cv2.resize(frame,(frame_width, frame_height))
        
        if len(position):
            for i in range(len(position)):
                source = (position[i][0], position[i][1])
                cv2.circle(frame,source, 10, (255, 0, 0), -1)

        cv2.imshow('window', frame)

        if cv2.waitKey(2) == 27:
            break  

def get_source_dest():
    if len(position)==2:
        source = (position[0][0]//grid_size, position[0][1]//grid_size)
        dest = (position[1][0]//grid_size , position[1][1]//grid_size)

        return source, dest

def intialize_tracker(cap):
    success, frame = cap.read()
    frame = cv2.resize(frame,(frame_width, frame_height))
    bbox = cv2.selectROI("window",frame, False)
    tracker.init(frame, bbox)

    return bbox

def get_qt_path_pts(planned_path):
    path = []

    for x, y in planned_path:
        path.append((x*grid_size, y*grid_size))


    qt = list()

    for x in range(len(planned_path)):
        i , j = planned_path[x]
        qt.append((i , j))

    pts = np.array(path , np.int32)

    return qt, path, pts

def draw_pos_info(img, x_est, y_est, tempx, tempy):
    cv2.circle(img,(int(x_est), int(y_est)), 2, (0, 255, 0), 5)
    cv2.putText(img, str(int(x_est)) + " "+ str(int(y_est)), (int(x_est), int(y_est)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,255 ), 2)

    cv2.circle(img,(int(tempx), int(tempy)), 10, (0, 255, 0), 5)
    cv2.circle(img,(int(tempx), int(tempy)), 15, (0, 255, 0), 5)
    cv2.putText(img, str(int(tempx)) + " "+ str(int(tempy)), (int(tempx), int(tempy)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255,255 ), 2)

def get_IMU_data(conn):
    dataString = str(conn.recv(BUFFER_SIZE))


    dataList = dataString.split(',')

    accelX, accelY, accelZ = dataList[0], dataList[1], dataList[2]
    gyroX, gyroY, gyroZ = dataList[3], dataList[4], dataList[5]
    magX, magY, magZ = dataList[6], dataList[7], dataList[8]
    temp = dataList[9]

    accel = {'x': accelX,
             'y': accelY,
             'z': accelZ
            }

    gyro = {'x': gyroX,
            'y': gyroY,
            'z': gyroZ
           }

    mag = {'x': magX,
           'y': magY,
           'z': magZ
          }

    return accel, gyro, mag, temp

def finish(conn, s, cap, SEND_COMMAND):
    s.send(SEND_COMMAND.encode())
    s.close()
    conn.close()
    cap.release()
    cv2.destroyAllWindows()

def main():
    SEND_COMMAND = STOP
    LAST_COMMAND = SEND_COMMAND

    # s, conn = make_connections()

    cap = cv2.VideoCapture(numCam)

    draw_source_dest(cap)
    source, dest = get_source_dest()

    occupied_grids, planned_path = process_image.main(source, dest, cap, grid_size, frame_width, frame_height, decision)

    qt, path, pts = get_qt_path_pts(planned_path)

    index = 0 # index of the list qt

    bbox = intialize_tracker(cap)

    cX, cY = 0, 0

    min_v = 500
    m_x, m_y = 0,0
    val = 0

    tempx, tempy = 0, 0

    # destination of the path to reach 
    final_x, final_y = qt[-1]

    (winW, winH) = (grid_size, grid_size)


    while True:

        # accel, gyro, mag, temp = get_IMU_data(conn)

        # print("accel: ", accel)
        # print("gyro: ", gyro)
        # print("mag: ", mag)
        # print("temp: ", temp)


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
        cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (20,20,230), 2);
     
        img = cv2.polylines(img, [pts] , False, (255,120,255), 3)

        
        xt = cX
        yt = cY

        if distance(xt, yt ,final_x, final_y) < grid_size:
            print("destination Reached")
            break


        if index < len(qt) - 1:
            # assume vehicle did not stop at any of the subgoal
            if distance(tempx, tempy ,xt, yt) < grid_size:
                print('next point')
                index += 1
                min_v = 500

            tempx, tempy = qt[index]
            tempx = tempx*grid_size
            tempy = tempy*grid_size
            x_est, y_est = xt, yt

            draw_pos_info(img, x_est, y_est, tempx, tempy)


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

        # to print the direcction of the car
        print('Action ' + direction[SEND_COMMAND])
     
        if LAST_COMMAND != SEND_COMMAND:# or timeElapsed % 3 == 0 :
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
    # finish(conn, s, cap, SEND_COMMAND)

if __name__ == '__main__':
    main()
