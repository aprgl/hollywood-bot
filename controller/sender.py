#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
import xbox_hid
context = zmq.Context()

controller = xbox_hid.xbox()

#  Socket to talk to server
print("Connecting to hello world server…")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

#  Do 10 requests, waiting each time for a response
for request in range(100):
    controller.update()
    report = controller.get_left_joystick()

    print(f"Sending request {request} …")
    socket.send_string(f"From Controller {report}")

    #  Get the reply.
    message = socket.recv()
    print(f"Received reply {request} [ {message} ]")