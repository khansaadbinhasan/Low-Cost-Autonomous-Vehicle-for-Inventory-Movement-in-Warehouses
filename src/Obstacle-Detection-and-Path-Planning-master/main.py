import process_image 
import cv2
import smooth
import numpy as np
import imutils
from collections import deque
import time
import socket
from parameters import numCam


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





position = []
def draw_circle(event , x, y, flags, param):
    global position
    if event == cv2.EVENT_LBUTTONDBLCLK:
        position.append((x, y))
        # print(mouseX/60, mouseY/60)

# for selecting source and destination

cap1 = cv2.VideoCapture(numCam)


'''
if len(position):
        print('sdivnjodi')
        for i in range(len(position)):
            source = (position[i][0], position[i][1])
            cv2.circle(frame1,source, 10, (255, 0, 0), -1)
'''

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




# print(path)

frame = np.zeros((640,640,3),np.uint8)

# res = list(zip(path , path[1:] + path[:1])) 
# print("printing the command for the car")
# command = list()
# for x in range(len(planned_path)-1) :
#     i, j = planned_path[x]
#     p, q = planned_path[x+1]

#     # print(i, " ", j, " " , p , " ", q)

#     if p==i+1:
#         command.append('L')
#     if p==i-1:
#         command.append('R')
#     if q==j+1:
#         command.append('F')
#     if q==j-1:
#         command.append('B')

# print(command)                                        

# qt = list()
# for x in range(len(planned_path)):
#     i , j = planned_path[x]
#     qt.append((i , j))


# result=smooth.smoothListGaussian(planned_path)
# print result
'''
path = [(1,1),(1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11), (1,12), (1,13), (1,14), (1,15) ]

print("smooth path of the estimated path is printed")
def behind(x, y, z):
    # if the first two points are on a vertical line
    if x[0] == y[0]:
        # if the third point is one the same vertical line?
        if y[0] == z[0]:
            # then they still need to be in the correct order
            return x[1] > y[1] > z[1] or x[1] < y[1] < z[1]
        else:
            return False
    elif y[0] == z[0]:
        return False
    # none of the points are directly above each other, calculate and compare direction
    return (x[1] - y[1]) / (x[0] - y[0]) == (y[1] - z[1]) / (y[0] - z[0])

print()
triples = list(zip(path[:-2], path[1:-1], path[2:]))
print(triples)
smooth_path = path[:1] + [
    y for x, y, z in triples
    if not behind(x, y, z)
] + path[-1:]

print(smooth_path)
'''

# print('print1')
cap = cv2.VideoCapture(numCam)

# cap = cv2.VideoCapture(numCam)

# blue = 110 - 130
color_l  = np.array([114, 57, 73])
color_h = np.array([148, 255, 255])

# pts = deque(maxlen=10)

index = 0 # index of the list qt

# for choosing the source and destination on the given frame
newx= 0
newy= 0
dest = [] #as destination always remains fixed
flag = 1
while True:

    # print('print2')

    _, frame = cap.read()

    # print('yahan tak to ho gya')

    frame = cv2.resize(frame,(640, 640))

    # blur = cv2.GaussianBlur(frame, (5,5),0)

    source = []
    if len(position)==2 and flag==1:
        newx = position[0][0]/64 
        newy = position[0][1]/64
        dest = (position[1][0]/64 , position[1][1]/64)
        flag=0

    source = (newx , newy)
    #print( source , dest)
    occupied_grids, planned_path = process_image.main(source , dest,cap)
    
    # print "Occupied Grids : "
    # print occupied_grids
    # print "Planned Path :"
    # print planned_path

    # print("actual coordinates")
    path = []
    for x, y in planned_path:
        path.append((x*64, y*64))



    pts = np.array(path , np.int32)

    new_frame= cv2.polylines(frame, [pts] , False, (255,120,255), 3)

    # _, frame = cap.read()

            # cv2.imshow("Frame", frame)
    cv2.imshow('window', new_frame)


    # blured_frame = cv2.GaussianBlur(frame, (5, 5) , 0)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # we are only allowing the given color range in the hsv model 
    kernel = np.ones((6,6), np.uint8)

    mask = cv2.inRange(hsv , color_l , color_h)
    
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.morphologyEx(mask , cv2.MORPH_OPEN, kernel)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # blurr the mask as well
    # bmask = cv2.GaussianBlur(mask, (5,5),0)
            
    red_mask = cv2.bitwise_and(frame, frame, mask = mask)

            #cv2.imshow("Frame", hsv)

    cnts,_= cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2:]
            # cv2.drawContours(frame, cnts , -1, (0,255,0), 2)
            # cnts = imutils.grab_contours(cnts)
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

    if xt!=0 or yt!=0:
        newx = xt
        newy = yt
    
    if xt==dest[0] and yt==dest[1]:
        print('reached to its destination')
        break

    if len(planned_path):
        if newx==planned_path[0][0]+1:
             SEND_COMMAND = LEFT
        elif newx==planned_path[0][0]-1:
             SEND_COMMAND = RIGHT
        elif newy==planned_path[0][1]+1:
             SEND_COMMAND = UP
        elif newy==planned_path[0][1]-1:
             SEND_COMMAND = DOWN


    print(SEND_COMMAND)
    s.send(str(SEND_COMMAND))

    '''
        if xt == tempx and yt==tempy:
            print(xt, yt)
            index+=1

    '''        

    # print(xt, yt)
    # print()
    # print(tempx , tempy)

    # if xt ==  tempx and yt == tempy:
        # print("reachead ")
        # index+=1
        #sent the next command from the list 
                
    # if index == len(qt):
        # break    
    if len(position):
        for i in range(len(position)):
            source = (position[i][0], position[i][1])
            cv2.circle(frame,source, 10, (255, 0, 0), -1)
        

    # cv2.imshow('mask', mask)
    # cv2.imshow('red_mask', red_mask)
    cv2.imshow('window', frame)


    k = cv2.waitKey(10) & 0xFF
    time.sleep(0.9)
    
    if k== 27:
        break 

    # cv2.imshow("path" , frame)

    # key=cv2.waitKey(1)

    # if key == ord('q'):
        # break
SEND_COMMAND = STOP 
s.send(str(SEND_COMMAND)) 
s.close() 
cap.release()
cv2.destroyAllWindows()





