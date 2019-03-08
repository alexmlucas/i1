# Search for BLE UART devices and list all that are found.
# Author: Tony DiCola
import atexit
import time
import uuid

import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART


# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

#UART_SERVICE_UUID = uuid.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
#TX_CHAR_UUID      = uuid.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')
#RX_CHAR_UUID      = uuid.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')


BNO_SERVICE_UUID = uuid.UUID('369B19D1-A340-497E-A8CE-DAFA92D76793')
YAW_CHAR_UUID      = uuid.UUID('9434C16F-B011-4590-8BE3-2F97D63CC549')
MOTOR_CHAR_UUID      = uuid.UUID('14EC9994-4932-4BDA-997A-B3D052CD7421')


# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))
    
    # start from a fresh state - disconnect all devices.
    UART.disconnect_devices()

    # Start scanning with the bluetooth adapter.
    adapter.start_scan()
    # Use atexit.register to call the adapter stop_scan function before quiting.
    # This is good practice for calling cleanup code in this main function as
    # a try/finally block might not be called since this is a background thread.
    atexit.register(adapter.stop_scan)
    print('Searching for UART devices...')
    print('Press Ctrl-C to quit (will take ~30 seconds on OSX).')
   
    counter = 0
    
    known_uarts = set()
    
    while counter < 5:
        found = set(UART.find_devices())
        new = found - known_uarts
        known_uarts.update(new)
        time.sleep(1)
        counter += 1
    
    for device in known_uarts:
        if device.name == 'BNO':
            device.connect()
            print("Now connected to {}".format(device.name))
            print(device.list_services())
    
    try:
        # Wait for service discovery to complete for at least the specified
        # service and characteristic UUID lists.  Will time out after 60 seconds
        # (specify timeout_sec parameter to override).
        print('Discovering services...')
        device.discover([BNO_SERVICE_UUID], [YAW_CHAR_UUID, MOTOR_CHAR_UUID])

        # Find the UART service and its characteristics.
        uart = device.find_service(BNO_SERVICE_UUID)
        yaw = uart.find_characteristic(YAW_CHAR_UUID)
        motor = uart.find_characteristic(MOTOR_CHAR_UUID)

        # Function to receive RX characteristic changes.  Note that this will
        # be called on a different thread so be careful to make sure state that
        # the function changes is thread safe.  Use queue or other thread-safe
        # primitives to send data to other threads.
        def received(data):
            print('Received: {0}'.format(data))

        # Turn on notification of RX characteristics using the callback above.
        print('Subscribing to RX characteristic changes...')
        yaw.start_notify(received)

        # Now just wait for 30 seconds to receive data.
        print('Waiting 60 seconds to receive data from the device...')
        time.sleep(60)
    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()
    
    print("Now disconnecting from {}".format(device.name))
    device.disconnect()
    

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
