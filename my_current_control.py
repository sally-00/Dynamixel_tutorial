#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Yi Zhang
#
# *********     Current control      *********
#
# Available Dynamixel model on this example : All models using Protocol 2.0
# This example is designed for using a Dynamixel XL330-M288-T, and an U2D2.
# To use another Dynamixel model, such as X series, see their details in E-Manual(emanual.robotis.com) and edit below variables yourself.
#

import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():            # gets the input which is for example code control.
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

os.sys.path.append('./DynamixelSDK-3.7.31/python/src')             # Path setting
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

import my_utils as utils
from my_global_variables_XL330M288T import *

dxl_goal_current            = 100                # Goal current. current limit is [0,1750]


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

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

utils.disable_torque(portHandler, packetHandler)

# Go to the position in the middle for a safe start
utils.go_to_middle_point(portHandler, packetHandler)

# Set control mode
utils.set_control_mode(CURRENT_CONTROL_MODE, portHandler, packetHandler)

# Enable Dynamixel Torque
utils.enable_torque(portHandler, packetHandler)

print("About to start control. Press any key to continue! (or press ESC to quit!)")
if getch() == chr(0x1b):
    exit()

# Read present position
dxl_present_position = utils.read_present_position(portHandler, packetHandler)

# Quit if close to position limit
"""
if dxl_present_position > DXL_MAXIMUM_POSITION_VALUE or dxl_present_position < DXL_MINIMUM_POSITION_VALUE:
    print("Near position limit! Quiting control...")
    exit()
"""
    
# Write goal current
utils.write_goal_current(dxl_goal_current, portHandler, packetHandler)
print("Setting goal current to ", utils.read_goal_current(portHandler, packetHandler))

# Continue control until KeyboardInterrupt
try:
    while 1:
        # Read present current
        dxl_present_current = utils.read_present_current(portHandler, packetHandler)
        print("[ID:%03d] GoalCurr:%03d  PresCurr:%03d" % (DXL_ID, dxl_goal_current, dxl_present_current))

except KeyboardInterrupt:
    # stop current control
    utils.write_goal_current(0, portHandler, packetHandler)


# Disable Dynamixel Torque
utils.disable_torque(portHandler, packetHandler)

# Close port
portHandler.closePort()
