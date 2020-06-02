numCam = 0

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

grid_size = 128
frame_height= 640
frame_width= 640
decision = 0


# Setting up TCP connection
TCP_IP = '192.168.43.208' # IP of raspberry pi
TCP_PORT = 5005
