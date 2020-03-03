#!/usr/bin/env python

'''
This program subscribes to multiple topics getting images as ros messages and converting them to cv2 images
Note: Do not imshow more than one image in callbacks.
'''




import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import os


numCams = 2;
bridge = CvBridge()


def main(args):
  rospy.init_node('image_converter', anonymous=True)
  
  image_sub = []

  map_dict = {
    'callback0': callback0,
    'callback1': callback1,
    'callback2': callback2,
    'callback3': callback3
  }

  # print(type(map_dict['callback1']))

  for i in range(numCams):
    image_sub.append(rospy.Subscriber("cam%d"%i,Image,map_dict['callback'+str(i)]))

  try:
    rospy.spin()

  except KeyboardInterrupt:
    print("Shutting down")

  cv2.destroyAllWindows()






def callback0(data0):

    try:
      cv_image0 = CvBridge().imgmsg_to_cv2(data0, "passthrough")

    except CvBridgeError as e:
      print(e)


    cv2.imshow('fra',cv_image0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
      os._exit(0)

def callback1(data1):

    try:
      cv_image1 = CvBridge().imgmsg_to_cv2(data1, "passthrough")

    except CvBridgeError as e:
      print(e)

def callback2(data2):

    try:
      cv_image2 = CvBridge().imgmsg_to_cv2(data2, "passthrough")

    except CvBridgeError as e:
      print(e)

def callback3(data3):

    try:
      cv_image3 = CvBridge().imgmsg_to_cv2(data3, "passthrough")

    except CvBridgeError as e:
      print(e)



if __name__ == '__main__':
    main(sys.argv)
