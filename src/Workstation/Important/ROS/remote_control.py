#!/usr/bin/python

'''
This program subscribes to image topic 'cam0' and sends control commands to the robot
'''

import pygame
import numpy as np
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import os
import socket


pygame.init()

bridge = CvBridge()

display_surface = pygame.display.set_mode((640, 480)) 
pygame.display.set_caption('Robot') 


STOP = '0'
UP = '1'
DOWN = '2'
RIGHT = '3'
LEFT = '4'

SEND_COMMAND = STOP

TCP_IP = '192.168.43.91' # IP of raspberry pi
TCP_PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))


def control_car(data):

    try:
      frame = CvBridge().imgmsg_to_cv2(data, "passthrough")

    except CvBridgeError as e:
      print(e)

    frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    frame = pygame.image.frombuffer(frame.tostring(), frame.shape[1::-1],"RGB")
    display_surface.blit(frame, (0, 0))


    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        os._exit(0)

    pressed = pygame.key.get_pressed()

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
      s.send(SEND_COMMAND)

    pygame.display.flip()
    pygame.display.update() 



def main(args):
  rospy.init_node('remote_control', anonymous=True)
  
  image_sub = rospy.Subscriber("cam0",Image,control_car)

  try:
    rospy.spin()

  except KeyboardInterrupt:
    print("Shutting down")


  s.close()

  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
