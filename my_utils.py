import os
import time

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

from my_global_variables_XL330M288T import *

def set_control_mode(mode, portHandler, packetHandler):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, mode)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been set to current control mode")

def enable_torque(portHandler, packetHandler):
    # Enable Dynamixel Torque
    # Dynamixel needs the TORQUE_ENABLE to be rotating or give you its internal information.
    # On the other hand, it doesn’t need torque enabled if you get your goal, so finally do TORQUE_DISABLE to prepare to the next sequence.
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")

def disable_torque(portHandler, packetHandler):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def read_present_position(portHandler, packetHandler):
    dxl_present_position, dxl_comm_result, dxl_error = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return dxl_present_position

def write_goal_position(goal_position, portHandler, packetHandler):
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, goal_position)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def read_present_current(portHandler, packetHandler):
    dxl_present_current, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_CURRENT)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return dxl_present_current

def read_goal_current(portHandler, packetHandler):
    dxl_goal_current, dxl_comm_result, dxl_error = packetHandler.read2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_CURRENT)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    return dxl_goal_current

def write_goal_current(dxl_goal_current, portHandler, packetHandler):
    dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_CURRENT, dxl_goal_current)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

def go_to_middle_point(portHandler, packetHandler):
    set_control_mode(POSITION_CONTROL_MODE, portHandler, packetHandler)
    enable_torque(portHandler, packetHandler)
    goal_position = int((DXL_MINIMUM_POSITION_VALUE + DXL_MAXIMUM_POSITION_VALUE) / 2)
    go_to_position(goal_position, portHandler, packetHandler)
    disable_torque(portHandler, packetHandler)

def go_to_position(goal_position, portHandler, packetHandler):
    # Write goal position
    write_goal_position(goal_position, portHandler, packetHandler)

    while 1:
        # Read present position
        dxl_present_position = read_present_position(portHandler, packetHandler)
        print("[ID:%03d] GoalPos:%03d  PresPos:%03d" % (DXL_ID, goal_position, dxl_present_position))

        if not abs(goal_position - dxl_present_position) > DXL_POSITION_MOVING_THRESHOLD:
            break

def check_read_freq(portHandler, packetHandler):
    # Check how many reading are done for one second
    count = 0
    ini_tic = time.perf_counter()
    while time.perf_counter() - ini_tic < 1:
        dxl_present_current = read_present_current(portHandler, packetHandler)
        count += 1
    print(count, " of readings are done in one second.")