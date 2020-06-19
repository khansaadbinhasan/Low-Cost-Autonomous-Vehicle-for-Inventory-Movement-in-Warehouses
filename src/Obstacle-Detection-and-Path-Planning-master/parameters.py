numCam = 1

STOP = '0'
UP = '1'
DOWN = '2'
RIGHT = '3'
LEFT = '4'


direction = {   STOP : "STOP",
                UP : "FORWARD",
                DOWN : "BACKWARD",
                RIGHT : "RIGHT",
                LEFT : "LEFT"
            }

grid_size = 32
frame_height= 640
frame_width= 640
decision = 0


# Setting up TCP connection for WASD control
TCP_IP_RPI = '192.168.43.208' # IP of raspberry pi
TCP_PORT_WASD = 5005


# Setting up TCP connection for getting IMU data
TCP_IP_WORKSTATION = '0.0.0.0'
TCP_PORT_IMU_DATA = 5007 # Port number on which to send data
BUFFER_SIZE = 200 # Normally 1024, but I want fast response



############### Tracker Types #####################

import cv2
 
#tracker = cv2.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
tracker = cv2.TrackerKCF_create()
#tracker = cv2.TrackerTLD_create()
#tracker = cv2.TrackerMedianFlow_create()
#tracker = cv2.TrackerCSRT_create()

# tracker = cv2.TrackerMOSSE_create()

minTheta = 15


stkr1minHSV = [0,196,206] 
stkr1maxHSV = [54,255,255]
stkr2minHSV = [102,51,29] 
stkr2maxHSV = [146,183,87]


# runAlgorithm = 'tracker'
runAlgorithm = 'heading'