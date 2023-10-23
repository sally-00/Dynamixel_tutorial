# Control table address
ADDR_OPERATING_MODE           = 11
ADDR_TORQUE_ENABLE            = 64               # Control table address is different in Dynamixel model
ADDR_GOAL_POSITION            = 116
ADDR_PRESENT_POSITION         = 132
ADDR_GOAL_CURRENT             = 102
ADDR_PRESENT_CURRENT          = 126


# Protocol version
PROTOCOL_VERSION              = 2.0               # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                        = 1                 # Dynamixel ID : 1
BAUDRATE                      = 57600             # Dynamixel default baudrate : 57600
DEVICENAME                    = '/dev/tty.usbserial-FT89FANK'    # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

CURRENT_CONTROL_MODE          = 0
POSITION_CONTROL_MODE         = 3
TORQUE_ENABLE                 = 1                 # Value for enabling the torque
TORQUE_DISABLE                = 0                 # Value for disabling the torque
DXL_MINIMUM_POSITION_VALUE    = 10                # Dynamixel will rotate between this value
DXL_MAXIMUM_POSITION_VALUE    = 4080              # and this value (note that the Dynamixel would not move when the position value is out of movable range. Check e-manual about the range of the Dynamixel you use.)
DXL_CURRENT_ERROR_THRESHOLD   = 10                 # Dynamixel moving status threshold
DXL_POSITION_MOVING_THRESHOLD = 10