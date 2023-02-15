import EasyPySpin
import cv2
import socket
import time
from imutils.video import VideoStream
import imagezmq
import numpy as np
import pyrealsense2 as rs

sender = imagezmq.ImageSender(connect_to='tcp://192.168.1.215:5555')

robot_hostname = socket.gethostname() # send robot hostname with each image

cap = EasyPySpin.VideoCapture(1)
cap2 = EasyPySpin.VideoCapture(0)

time.sleep(2.0)  # allow camera sensor to warm up

while True:  # send images as stream until Ctrl-C
    # Reading an image in default mode
    ret, left_eye = cap.read()
    ret2, right_eye = cap2.read()
      
    # Window name in which image is displayed
    window_name = 'Hollywood Eyes'

    # concatenate image Horizontally
    Hori = np.concatenate((right_eye, left_eye), axis=1)


    sender.send_image(robot_hostname, Hori)

cv2.destroyAllWindows()
cap.release()