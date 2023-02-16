#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq
import struct

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

while True:
    #  Wait for next request from client
    message = socket.recv()
    depacket = struct.unpack('HH', message)
    #print(f"Received request: {depacket}")

    # Axis          Min     Max     Range   Midpoint    Multplier
    # Head rotate   450     3328    2878    1889        0.04391546502
    # Head tilt     1750    2463    713     2106        0.01087968261
    
    head_rotate_target = int((depacket[0] * 0.04391546502) + 450)
    head_tilt_target = int((depacket[1] * 0.01087968261) + 1750)
    
    print(head_rotate_target, head_tilt_target)

    if(head_rotate_target > 3328):
        head_rotate_target = 3328

    if(head_rotate_target < 450):
        head_rotate_target = 450

    if(head_tilt_target > 2463):
        head_tilt_target = 2463

    if(head_tilt_target < 1750):
        head_tilt_target = 1750

    print("after", head_rotate_target, head_tilt_target)


    socket.send(b"Ack")