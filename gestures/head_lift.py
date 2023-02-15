#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, time

NUM_WAVES = 7

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import *                    # Uses Dynamixel SDK library

MY_DXL = 'X_SERIES'       # X330 (5.0 V recommended), X430, X540, 2X430

# Control table address
if MY_DXL == 'X_SERIES' or MY_DXL == 'MX_SERIES':
    ADDR_TORQUE_ENABLE          = 64
    ADDR_LED_RED                = 65
    LEN_LED_RED                 = 1         # Data Byte Length
    ADDR_GOAL_POSITION          = 116
    LEN_GOAL_POSITION           = 4         # Data Byte Length
    ADDR_PRESENT_POSITION       = 132
    LEN_PRESENT_POSITION        = 4         # Data Byte Length
    DXL_MINIMUM_POSITION_VALUE  = 0         # Refer to the Minimum Position Limit of product eManual
    DXL_MAXIMUM_POSITION_VALUE  = 4095      # Refer to the Maximum Position Limit of product eManual
    BAUDRATE                    = 57600

# DYNAMIXEL Protocol Version (1.0 / 2.0)
# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0

# Make sure that each DYNAMIXEL ID should have unique ID.
HEAD_TILT_ID            = 3
HEAD_ROTATE_ID          = 4
WRIST_ADD_R_ID          = 5
WRIST_SUP_R_ID          = 6
WRIST_FLEX_R_ID         = 7
ARM_ADD_R_ID            = 8
SHOULDER_ROT_R_ID       = 9
ELBOW_R_ID              = 10
SHOULDER_ADD_R_ID       = 11

# Use the actual port assigned to the U2D2.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = '/dev/tty.usbserial-FT4TFLVY'

TORQUE_ENABLE               = 1                 # Value for enabling the torque
TORQUE_DISABLE              = 0                 # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20                # Dynamixel moving status threshold

index = 0

#Robot Wave Positions
ht_goal_positions = [2093, 2093]
hr_goal_positions = [1903, 1903]
war_goal_positions = [2531,3169]
wsr_goal_positions = [1449, 1449]
wfr_goal_positions = [2326,2326]
aar_goal_positions = [658, 658]
srr_goal_positions = [1024, 1024]
er_goal_positions = [2024, 2946]
sar_goal_positions = [4000, 4000]


dxl_led_value = [0x00, 0x01]                                                        # Dynamixel LED value for write

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Initialize GroupBulkWrite instance
groupBulkWrite = GroupBulkWrite(portHandler, packetHandler)

# Initialize GroupBulkRead instace for Present Position
groupBulkRead = GroupBulkRead(portHandler, packetHandler)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()



# Enable Torques
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, HEAD_TILT_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % HEAD_TILT_ID)

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, HEAD_ROTATE_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel#%d has been successfully connected" % HEAD_ROTATE_ID)

# Add parameter storage for Dynamixel#1 present position
dxl_addparam_result = groupBulkRead.addParam(HEAD_TILT_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
if dxl_addparam_result != True:
    print("[ID:%03d] groupBulkRead addparam failed" % HEAD_TILT_ID)
    quit()

dxl_addparam_result = groupBulkRead.addParam(HEAD_ROTATE_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
if dxl_addparam_result != True:
    print("[ID:%03d] groupBulkRead addparam failed" % HEAD_ROTATE_ID)
    quit()

waves = 0

while waves < NUM_WAVES:
    print("Press any key to continue! (or press ESC to quit!)")
    #if getch() == chr(0x1b):
    #    break
    time.sleep(0.2)

    # Allocate goal position value into byte array
    ht_goal_position = [DXL_LOBYTE(DXL_LOWORD(ht_goal_positions[index])), DXL_HIBYTE(DXL_LOWORD(ht_goal_positions[index])), DXL_LOBYTE(DXL_HIWORD(ht_goal_positions[index])), DXL_HIBYTE(DXL_HIWORD(ht_goal_positions[index]))]
    hr_goal_position = [DXL_LOBYTE(DXL_LOWORD(hr_goal_positions[index])), DXL_HIBYTE(DXL_LOWORD(hr_goal_positions[index])), DXL_LOBYTE(DXL_HIWORD(hr_goal_positions[index])), DXL_HIBYTE(DXL_HIWORD(hr_goal_positions[index]))]


    # Add goal position value to the Bulkwrite parameter storage
    dxl_addparam_result = groupBulkWrite.addParam(HEAD_TILT_ID, ADDR_GOAL_POSITION, LEN_GOAL_POSITION, ht_goal_position)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupBulkWrite addparam failed" % HEAD_TILT_ID)
        quit()

    dxl_addparam_result = groupBulkWrite.addParam(HEAD_ROTATE_ID, ADDR_GOAL_POSITION, LEN_GOAL_POSITION, hr_goal_position)
    if dxl_addparam_result != True:
        print("[ID:%03d] groupBulkWrite addparam failed" % HEAD_ROTATE_ID)
        quit()
 

    # Bulkwrite goal position and LED value
    dxl_comm_result = groupBulkWrite.txPacket()
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))

    # Clear bulkwrite parameter storage
    groupBulkWrite.clearParam()

    if waves == 0 and index == 0:
        time.sleep(3)

    while 1:
        # Bulkread present position and LED status
        dxl_comm_result = groupBulkRead.txRxPacket()
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
            print("Booo")

        # Check if groupbulkread data is available
        dxl_getdata_result = groupBulkRead.isAvailable(HEAD_TILT_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % HEAD_TILT_ID)
            #quit()
        dxl_getdata_result = groupBulkRead.isAvailable(HEAD_ROTATE_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        if dxl_getdata_result != True:
            print("[ID:%03d] groupBulkRead getdata failed" % HEAD_ROTATE_ID)
            #quit()


        # Get present position value
        ht_present_position = groupBulkRead.getData(HEAD_TILT_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)
        hr_present_position = groupBulkRead.getData(HEAD_ROTATE_ID, ADDR_PRESENT_POSITION, LEN_PRESENT_POSITION)

        print("[ID:%03d] Present Position : %d" % (HEAD_TILT_ID, ht_present_position))
        print("[ID:%03d] Present Position : %d" % (HEAD_ROTATE_ID, hr_present_position))

        break

    # Change goal position
    if index == 0:
        index = 1
    else:
        index = 0
        waves += 1

time.sleep(0.2);

# Clear bulkread parameter storage
groupBulkRead.clearParam()


# Disable Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, HEAD_TILT_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))

dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, HEAD_ROTATE_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))


# Close port
portHandler.closePort()
