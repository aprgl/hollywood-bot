import hid

for device in hid.enumerate():
    print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

gamepad = hid.device()
gamepad.open(0x045e, 0x0b13)
gamepad.set_nonblocking(True)


# Notes 
# - Y Joysticks is max at bottom, zero at top of controller
# - X Joysticks is max at right, zero at left

# ----- Analog Devices ----- #
left_joystick_x = 0
left_joystick_y = 0
right_joystick_x = 0
right_joystick_y = 0
left_trigger = 0 
right_trigger = 0


arrows = 0
arrow_up = 0x01
arrow_right = 0x03
arrow_down = 0x05
arrow_left = 0x07

buttons = 0
a_btn = 0x01
b_btn = 0x02
x_btn = 0x08
y_btn = 0x10 #16
left_bumper = 0x40  #64
right_bumper = 0x80 #128

# Last two button packing is a bit underfilled

buttons2 = 0
left_joystick_depress = 0x20   #32
right_joystick_depress = 0x40  #64

buttons3 = 0
back_button = 0x01

while True:

    report = gamepad.read(64)
    #if(report):
        #print(report)

    if(len(report) == 17):        
        left_joystick_x = report[2]<<8 | report[1]
        left_joystick_y = report[4]<<8 | report[3]
        right_joystick_x = report[6]<<8 | report[5]
        right_joystick_y = report[8]<<8 | report[7]
        left_trigger = report[10]<<8 | report[9]
        right_trigger = report[12]<<8 | report[11]
        arrows = report[13]
        buttons = report[14]
        buttons2 = report[15]
        buttons3 = report[16]

        print(left_joystick_x, left_joystick_y, right_joystick_x, right_joystick_y, left_trigger, right_trigger)
        #print('[{}]'.format(', '.join(hex(x) for x in report)))
