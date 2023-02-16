# Send the commands from the controller to the robot's brainbucket

import zmq
import xbox_hid

import struct

context = zmq.Context()

controller = xbox_hid.xbox()
print("Connecting Bot-Hollywood")

socket = context.socket(zmq.REQ)
socket.connect("tcp://192.168.1.108:5555") #localhost for testing

#  Do 10 requests, waiting each time for a response

last_packet = 0
while True:
    controller.update()
    report = controller.get_left_joystick()
    packet = struct.pack('HH', report[0], report[1])
    if (packet != last_packet):
        socket.send(packet)
        last_packet = packet
    
        #print(f"Sending request {packet} …")
        

        #  Get the reply.
        message = socket.recv()
        #print(f"Received reply {packet} [ {message} ]")