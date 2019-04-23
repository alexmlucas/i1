import time
import uuid
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART

# define in seconds how long to scan for bluetooth UART devices
BLUETOOTH_CONNECTION_TIMER = 3

# define uuid's used by wristband
BNO_SERVICE_UUID = uuid.UUID('369B19D1-A340-497E-A8CE-DAFA92D76793')
YAW_CHAR_UUID    = uuid.UUID('9434C16F-B011-4590-8BE3-2F97D63CC549')
MOTOR_CHAR_UUID  = uuid.UUID('14EC9994-4932-4BDA-997A-B3D052CD7421')

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

yaw = None

# Function to receive RX characteristic changes.
# this function is passed to the start_nofify method of the yaw characteristic
def received(data):
    print('Received: {0}'.format(data))

    
def get_bno_device(incoming_adapter):    
    try:
        # start scanning with the bluetooth adapter
        incoming_adapter.start_scan()
        # keep track of the time spent scanning bluetooth UART devices
        bluetooth_counter = 0
        # intialise a set to contain known UARTs
        known_uart_devices = set()
        # keep track of whether or not the BNO uart device has been found
        bno_found_flag = False
        
        while bno_found_flag == False:
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
            
            # now that we have a list of UART devices, look for the BNO device
            for device in known_uart_devices:
                if device.name == 'BNO':
                    # the bno device has been found, now connect to it.
                    device.connect()
                    # disconnect device on program exit
                    print("Now connected to {}".format(device.name))
                    # now that the bno is found, set the flag to true.
                    bno_found_flag = True
                    device_to_return = device
            
            if bno_found_flag == True:
                break

            # if the code reaches this point then the bno device has not been found, therefore we will loop again.
            print('BNO device not found, continuing to search')
            
    finally:
        # Make sure scanning is stopped before moving on to the next block of code
        incoming_adapter.stop_scan()
        return device_to_return
        
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
    # start from a fresh state - disconnect all bluetooth UART devices.
    UART.disconnect_devices()
    # scan uarts, connect to BNO if found
    bno_device = get_bno_device(adapter)
    # get the yaw characteristic from the bno device
    yaw = get_yaw_characteristic(bno_device)
    # subscribe to changes in yaw charcteristic
    yaw.start_notify(received)
    
    # start the main loop
    print('running main loop')
    
    while True:
        time.sleep(1)

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
