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

class Wristband:
	# Get the BLE provider for the current platform.
	ble = Adafruit_BluefruitLE.get_provider()
	
	def __init__ (self):
		###### INITIALISE BLUETOOTH ######
		# Clear any cached data.
		ble.clear_cached_data()
		# Get the first available BLE network adapter
		self.adapter = ble.get_default_adapter()
		# power on the bluetooth adapter
		self.adapter.power_on()
		# start from a fresh state - disconnect all bluetooth UART devices.
		UART.disconnect_devices()
		
	def search_and_connect(self):
		###### SEARCH FOR BNO AND CONNECT IF FOUND ######
		try:
			# start scanning with the bluetooth adapter
			self.adapter.start_scan()
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
						print("Now connected to {}".format(device.name))
						# now that the bno is found, set the flag to true.
						bno_found_flag = True
				
				if bno_found_flag == True:
					break

				# if the code reaches this point then the bno device has not been found, therefore we will loop again.
				print('BNO device not found, continuing to search')
				
		finally:
			# Make sure scanning is stopped before moving on to the next block of code
			adapter.stop_scan()
		
		
