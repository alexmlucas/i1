import serial
import csv
import time
import uuid
import pygame

import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

# Custom class includes
from parameter_manager import *
from guitar import *
from song_player import *

# define in seconds how long to scan for bluetooth UART devices
BLUETOOTH_CONNECTION_TIMER = 3

# define uuid's used by wristband
BNO_SERVICE_UUID = uuid.UUID('369B19D1-A340-497E-A8CE-DAFA92D76793')
YAW_CHAR_UUID    = uuid.UUID('9434C16F-B011-4590-8BE3-2F97D63CC549')
MOTOR_CHAR_UUID  = uuid.UUID('14EC9994-4932-4BDA-997A-B3D052CD7421')

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

# Global parameters
NOTE_VELOCITY = 100
NOTE_LENGTH = 0.5

# Classes
parameter_manager = Parameter_Manager('/dev/serial0', 9600)
guitar = Guitar(1, NOTE_VELOCITY, NOTE_LENGTH)

current_song = parameter_manager.get_global_parameter('b')
song_player = Song_Player(current_song)
song_player.set_play_state(1)

guitar.set_zone_notes(0, 0)
guitar.set_zone_notes(0, 1)
guitar.set_zone_notes(0, 2)
guitar.set_zone_notes(0, 3)

yaw = None
initialisation_flag = True

# initialise the BNO device to NULL
bno_device = None

# Function to receive RX characteristic changes.
# this function is passed to the start_nofify method of the yaw characteristic
def received(data):
    print('Received: {0}'.format(data))
    
    # get the current zone
    current_zone = parameter_manager.get_song_parameter('l')
    
    if data != "-1.":
        guitar.play_string(current_zone, int(float(data)))
    
def get_bno_device(incoming_adapter):    
    # get a global reference to the bno_device
    global bno_device

    # start from a fresh state - disconnect all bluetooth UART devices.
    UART.disconnect_devices()
    
    # start scanning with the bluetooth adapter
    incoming_adapter.start_scan()
    
    # keep track of the time spent scanning bluetooth UART devices
    bluetooth_counter = 0
    
    # intialise a set to contain known UARTs
    known_uart_devices = set()
    
    # keep track of whether or not the BNO uart device has been found
    bno_found_flag = False
    
    print('Searching for UART devices...')
    while bluetooth_counter <= BLUETOOTH_CONNECTION_TIMER:
        # create a set of all UART devices currently visable
        found_uart_devices = set(UART.find_devices())
        # identify any new devices by subtracting previously known devices from those just found
        new_uart_devices = found_uart_devices - known_uart_devices
        # add any new devices to the known device list
        known_uart_devices.update(new_uart_devices)
        # pause for one second prior to the next interation of the loop
        time.sleep(1)
        print("{} seconds elasped".format(bluetooth_counter))
        bluetooth_counter += 1
    
    # stop the scan
    incoming_adapter.stop_scan()
    
    # now that we have a list of UART devices, look for the BNO device
    for device in known_uart_devices:
        if device.name == 'BNO':
            # the bno device has been found, now connect to it.
            device.connect()
            # make sure you disconnect device on program exit!!
            print("Now connected to {}".format(device.name))
            # assign the bno_device
            bno_device = device
            # get the yaw characteristic from the bno device
            yaw = get_yaw_characteristic(bno_device)
            # subscribe to changes in yaw charcteristic
            yaw.start_notify(received)

def get_yaw_characteristic(incoming_device):
    print(incoming_device)
    print('Discovering services...')
    incoming_device.discover([BNO_SERVICE_UUID], [YAW_CHAR_UUID, MOTOR_CHAR_UUID])

    # Assign the UART service and its characteristics to variables.
    uart = incoming_device.find_service(BNO_SERVICE_UUID)
    yaw = uart.find_characteristic(YAW_CHAR_UUID)
    motor = uart.find_characteristic(MOTOR_CHAR_UUID)
    return yaw

def main():
    # Clear any cached data.
    ble.clear_cached_data()
    
    # Get the first available BLE network adapter
    adapter = ble.get_default_adapter()
    
    # power on the bluetooth adapter
    adapter.power_on()
    
    # get the bno device
    get_bno_device(adapter)
   
    print("entering the main loop")
    
    while True:
        # This is the main loop
        # Control surface should initialise automatically when in this loop.
        parameter_manager.check_incoming()

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
