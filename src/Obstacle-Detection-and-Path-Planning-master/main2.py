import cv2, imutils
import numpy as np
import socket
import time
import rst

# from numpy import array, dot, arccos, clip
# from numpy.linalg import norm


import process_image
from parameters import numCam, STOP, UP, DOWN, RIGHT, LEFT, direction, grid_size, frame_height, frame_width, decision, TCP_IP_RPI, TCP_PORT_WASD, TCP_IP_WORKSTATION, TCP_PORT_IMU_DATA, BUFFER_SIZE, tracker, minTheta


position = []
tempx = 0
tempy = 0
index = 0

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

    return s1

    # s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s2.bind((TCP_IP_WORKSTATION, TCP_PORT_IMU_DATA))
    # s2.listen(1)

    # conn, addr = s2.accept()
    # print ('Connection address:', addr)

    # return s1, conn

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

def destination_reached(cX, cY ,final_x, final_y):
    if distance(cX, cY ,final_x, final_y) < grid_size:
        return True

    return False


def get_cmd(cX, cY, min_v, tempx, tempy):
    cmd = STOP

    p1_x, p1_y = cX + 1, cY 
    p2_x, p2_y = cX - 1, cY 
    p3_x, p3_y = cX , cY +1
    p4_x, p4_y = cX , cY -1

    dis1 = distance(p1_x, p1_y, tempx, tempy)
    dis2 = distance(p2_x, p2_y, tempx, tempy)
    dis3 = distance(p3_x, p3_y, tempx, tempy)
    dis4 = distance(p4_x, p4_y, tempx, tempy)

    if dis1 < min_v:
        min_v = dis1
        cmd = RIGHT

    if dis2 < min_v:
        min_v = dis2
        cmd = LEFT

    if dis3 < min_v:
        min_v = dis3
        cmd = DOWN

    if dis4 < min_v:
        min_v = dis4
        cmd = UP

    return cmd

def update_tracker_data(tracker, img):
    success, bbox = tracker.update(img)

    cX = 0
    cY = 0
 
    if success:
        drawBox(img,bbox)
        
        # cX = int(bbox[0] + (bbox[2]/2))
        # cY = int(bbox[1] + (bbox[3]/2))

        cX = int((bbox[0] + bbox[2])/2)
        cY = int((bbox[1] + bbox[3])/2)

        cv2.putText(img,str(cX) + " " +str(cY), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    else:
        cv2.putText(img, "Lost", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
 
    # cv2.rectangle(img,(15,15),(200,90),(255,0,255),2)

    return cX, cY



def make_grids(img, grid_size, winW, winH):
    # this code is used for making grids
    for (x, y, window) in process_image.sliding_window(img, stepSize=grid_size, windowSize=(winW, winH)):
        # if the window does not meet our desired window size, ignore it
        if window.shape[0] != winH or window.shape[1] != winW:
            continue

        cv2.rectangle(img, (x, y), (x + winW, y + winH), (0, 255, 0), 2)


# def finish(conn, s, cap, SEND_COMMAND):
def finish(s, cap, SEND_COMMAND):
    s.send(SEND_COMMAND.encode())
    s.close()
    # conn.close()
    cap.release()
    cv2.destroyAllWindows()


def angle_between(u, v):
    c = np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v) 
    angle = np.arccos(np.clip(c, -1, 1)) 
    angle_degs = np.degrees(angle)


    c = np.cross(v,u)/np.linalg.norm(u)/np.linalg.norm(v) 
    angle_sin = np.arcsin(np.clip(c, -1, 1)) 

    if angle_sin < 0:
        return -1*angle_degs


    return angle_degs


def get_result(u,v):
    
    angle_btw = angle_between(u,v)

    print(angle_btw)

    result = STOP

    if angle_btw > 180 - minTheta and angle_btw < 180 + minTheta:
        result = UP

    elif angle_btw < 180 - minTheta and angle_btw > minTheta:
        result = LEFT

    elif angle_btw > -(180 - minTheta) and angle_btw < -minTheta:
        result = RIGHT

    elif angle_btw < minTheta and angle_btw > -minTheta:
        result = DOWN

    else:
        result = STOP

    return result


def send_command(s, LAST_COMMAND, SEND_COMMAND):
    if LAST_COMMAND != SEND_COMMAND:
        s.send(SEND_COMMAND.encode())
        LAST_COMMAND = SEND_COMMAND


    return LAST_COMMAND


def draw_circle_on_source(img, path):
    if len(path):
        for i in range(len(path)):
            source = (path[i][0], path[i][1])

            if i == 0 or i == len(path) - 1:
                cv2.circle(img,source, 2, (255, 0, 0), 10)

            else:
                cv2.circle(img,source, 2, (255, 0, 0), 2)

def run_tracker_algo(tracker, img, final_x, final_y, qt, grid_size, min_v):
    global index, tempx, tempy

    SEND_COMMAND = STOP

    cX, cY = update_tracker_data(tracker, img)

    #This function is not working correctly
    if destination_reached(cX, cY ,final_x, final_y):
        print("destination Reached")
        return 'done'


    if index < len(qt) - 1:
        # assume vehicle did not stop at any of the subgoal
        if distance(tempx, tempy ,cX, cY) < grid_size:
            index += 1
            min_v = 500

        tempx, tempy = qt[index]
        tempx, tempy = tempx*grid_size, tempy*grid_size

        draw_pos_info(img, cX, cY, tempx, tempy)
        SEND_COMMAND = get_cmd(cX, cY, min_v, tempx, tempy)

    return SEND_COMMAND


def run_heading_algo(img, o1,o2, p1, p2, qt):
    x1, y1 = 0, 0
    x2, y2 = 0, 0

    try:
        # for drawing the matrix on to the frame
        x1, y1, _ = rst.get_moments(img, o1, o2, 1)
        x2, y2, _ = rst.get_moments(img, p1, p2, 2)

    except:
        pass

    xt = (x1+x2)//2
    yt = (y1+y2)//2

    cv2.circle(img,(int(xt), int(yt)), 2, (0, 255, 0), 5)

    next_x, next_y = next_point(img, qt, xt, yt)
    
    if (next_x == -1 and next_y == -1):
        print("destination Reached")
        SEND_COMMAND = 'done'

    u = ( x2 - x1, y2 - y1 )
    v = ( xt - next_x, yt - next_y )

    SEND_COMMAND = get_result(u,v)

    img = cv2.line(img,(x1, y1),(x2, y2), (0,255,0), 3)
    img = cv2.line(img, (xt, yt),(next_x, next_y),(0,0,255), 3)


    return SEND_COMMAND



def main():
    SEND_COMMAND = STOP
    LAST_COMMAND = SEND_COMMAND

    s = make_connections()

    cap = cv2.VideoCapture(numCam)

    draw_source_dest(cap)
    source, dest = get_source_dest()

    occupied_grids, planned_path = process_image.main(source, dest, cap, grid_size, frame_width, frame_height, decision)

    qt, path, pts = get_qt_path_pts(planned_path)

    index = 0 # index of the list qt

    # bbox = intialize_tracker(cap)

    cX, cY = 0, 0

    min_v = 500
    m_x, m_y = 0,0
    cmd = 0

    tempx, tempy = 0, 0

    # destination of the path to reach 
    final_x, final_y = qt[-1]

    (winW, winH) = (grid_size, grid_size)



    # colors that need to adjusted

    o1 = [0,196,206] # green sticker
    o2 = [54,255,255]
    p1 = [102,51,29] # blue sticker
    p2 = [146,183,87]


    while True:

        # accel, gyro, mag, temp = get_IMU_data(conn)

        timer = cv2.getTickCount()
        _, img = cap.read()
        img = cv2.resize(img,(frame_width, frame_height))

        draw_circle_on_source(img, path)
        make_grids(img, grid_size, winW, winH)

        img = cv2.polylines(img, [pts] , False, (255,120,255), 3)

        # SEND_COMMAND = run_tracker_algo(tracker, img, final_x, final_y, qt, grid_size, min_v)
        SEND_COMMAND = run_heading_algo(img, o1,o2, p1, p2, qt)
        LAST_COMMAND = send_command(s, LAST_COMMAND, SEND_COMMAND)



        if SEND_COMMAND == 'done':
            break

        # to print the direcction of the car
        print('Action ' + direction[SEND_COMMAND])
        

        # LAST_COMMAND = send_command(s, LAST_COMMAND, SEND_COMMAND)
        # draw_circle_on_source(img, path)
 
        
        cv2.imshow('window', img)

        if cv2.waitKey(2) & 0xFF == 27:
            break 


    SEND_COMMAND = STOP
    finish(s, cap, SEND_COMMAND)
    # finish(conn, s, cap, SEND_COMMAND)

if __name__ == '__main__':
    main()
