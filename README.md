# Dynamixel tutorial

This repository includes the Dynamixel library and python sample code for position and current control.
You can use most of the languages with Dynaimxel SDK. If using other Dynamixel model, you need to change addresses in `my_global_variables_XL330M288T.py` according to your model.

- OS: Mac OS / Windows / Linux
- Language: Python
- Dynamixel model: XL330-M288T 

## Quick start
1. Download this repository.
2. Set up hardware as described in `Dynamixel_tutorial.pdf`
3. Run `dynamixel_sdk_sample_read_write.py` to try position control. Or, run `my_current_control.py` to try current/torque control. 
    (You might need to change `DEVICENAME` in `my_global_variables_XL330M288T.py` if not using Mac. Refer to the last page in `Dynamixel_tutorial.pdf`)

## Tutorial
`Dynamixel_tutorial.pdf` for instructions on hardware setup, package download and running sample code.

## Sample code
`dynamixel_sdk_sample_read_write.py` is a sample code given by dynamixel (modofied).
`my_current_control.py` is a sample code for current control.

## Tips

A few tips from my shallow experience with Dynamixel...

#### DYNAMIXEL Wizard applicaiton

The application cannot be used while running code to communicate with DYNAMIXEL.

#### Enable torque

You need to 'enable torque' (writing TORQUE_ENABLE to ADDR_TORQUE_ENABLE) to access dynamixel internal information.

However, after enabling torque, a lot of settings are locked (you cannot write information to change them). To see what information is locked: enable torque on DYNAMIXEL Wizard application and check the control table on the app.

Thus,
- Set operating mode and various limits etc. (all the parameters that will be lock) before enabling torque.
- You might need to disable torque at the beginning of the code, if it was not disabled properly after last operation.

#### Reading and Writing information

The code to control dynamixel is basically reading and writing information at specific addresses which are defined in control table on each model's page (ex. [XL330-M288-T](https://emanual.robotis.com/docs/en/dxl/x/xl330-m288/#control-table-description)).
Size (Bytes) of the data is also specified on the control table. 

For example, use `information, result, error = read4ByteTxRx(portHandler, Dynamixel_ID, Address_number)` to read a 4 byte information from Address_number, use `result, error = packetHandler.write2ByteTxRx(portHandler, Dynamixel_ID, Address_number, information)` to write information to Address_number which has a 2 byte size.

## On-going Problem

In `my_current_control.py`, cannot disable torque when trying to stop the control.

It shows: `[TxRxResult] Port is in use!`.

Current solution: switch off the power to motor and disable torque at the beginning of the code.