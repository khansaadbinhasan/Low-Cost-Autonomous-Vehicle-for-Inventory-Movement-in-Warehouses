'''
This python script can be used to remotely control the robot.
        --> Sets up a TCP connection with RPI.
        --> Gets Video stream from RPI.
        --> Able to send forward, backward, right, left and stop commands to arduinio via rpi 
'''


import pygame
import cv2
import numpy as np
import socket


pygame.init()
done = False

display_surface = pygame.display.set_mode((640, 480)) 
pygame.display.set_caption('Robot') 


STOP = '0'
UP = '1'
DOWN = '2'
RIGHT = '3'
LEFT = '4'

SEND_COMMAND = STOP
LAST_COMMAND = SEND_COMMAND


# Setting up TCP connection
TCP_IP = '192.168.43.208' # IP of raspberry pi
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


cap = cv2.VideoCapture(0) # Port on which rpi is sending the video stream

clock = pygame.time.Clock()


while not done:
        # Getting video from RPI
        ret, frame = cap.read()
        
        frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        frame = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1],"RGB")

        display_surface.blit(frame, (0, 0))


        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        pressed = pygame.key.get_pressed()


        # If key is pressed send appropriate commands
        if np.count_nonzero(pressed) > 0:

                if pressed[pygame.K_UP]: 
                        SEND_COMMAND = UP

                elif pressed[pygame.K_DOWN]: 
                        SEND_COMMAND = DOWN

                elif pressed[pygame.K_LEFT]: 
                        SEND_COMMAND = LEFT

                elif pressed[pygame.K_RIGHT]: 
                	SEND_COMMAND = RIGHT

                elif pressed[pygame.K_SPACE]:
                        SEND_COMMAND = STOP

                else:
                        SEND_COMMAND = STOP


                        
                print(SEND_COMMAND)
                s.send(bytes(SEND_COMMAND,encoding="UTF-8"))

                        

        pygame.display.flip()
        clock.tick(60)
        pygame.display.update() 


s.close()
cap.release()
cv2.destroyAllWindows()