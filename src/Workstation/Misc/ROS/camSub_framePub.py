#!/usr/bin/env python

'''
This program takes in the ip addresses of all cameras as a list and the number of cameras and publishes the cv2 images as ros messages on cam topics.
'''

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image 
import cv2
from cv_bridge import CvBridge, CvBridgeError
import sys
from imutils.video import FileVideoStream
from imutils.video import FPS
import numpy as np
import imutils


def main(args):
  rospy.init_node('camSub_framePub', anonymous=True)
  bridge = CvBridge()
  

  # camsIPs = ['udp://localhost:8009', 'udp://localhost:8010', 'udp://localhost:8011']
  # numcams = 1
  camsIPs = [0]
  numcams = 1


  # open a pointer to the video stream and start the FPS timer
  stream = []
  fps = []
  image_pub = []
  num = 0

  for ip in camsIPs:
    streaming = cv2.VideoCapture(ip)
    
    stream.append(streaming)
    fps.append(FPS().start())
    image_pub.append(rospy.Publisher("cam%d"%num,Image, queue_size=10))

    num = num + 1


  try:
    # loop over frame2s from the video file stream
    while True:
      grabbed = []
      frames = []
      image_message = []

      for i in range(numcams):
        # grab the frames from the threaded video file stream
        (grabbing, framing) = stream[i].read()

        grabbed.append(grabbing), frames.append(framing)
      
        # print()

        if not grabbing:
          print("\n"*5,"camera %d frame not grabbed"%i)
          break
      
      
        # show the frame and update the FPS counter
        cv2.imshow("Frame%d"%i, frames[i])
        

        image_message.append(bridge.cv2_to_imgmsg(np.uint8(frames[i]), encoding="passthrough"))
        image_pub[i].publish(image_message[i])

      fps[i].update()

      if cv2.waitKey(1) & 0xFF == ord('q'):
        break

  except KeyboardInterrupt:
    print("Shutting down")


  
  for i in range(numcams):
  
    fps[i].stop()
    print("[INFO] elasped time: {:.2f}".format(fps[i].elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps[i].fps()))

    stream[i].release()


  cv2.destroyAllWindows()


if __name__ == '__main__':
    main(sys.argv)