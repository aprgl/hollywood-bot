import EasyPySpin
import cv2
import socket
import time
from imutils.video import VideoStream
import imagezmq
import numpy as np
import pyrealsense2 as rs


# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()



# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))


found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)



config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

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