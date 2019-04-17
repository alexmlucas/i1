import serial
import time

# Connect to serial port
control_board = serial.Serial('/dev/tty.usbmodem14111', 2000000, timeout=0.1)

# Flush serial inputs and outputs.
control_board.flushInput()
control_board.flushOutput()

# Request data from sip puff sensor.
# request_string  = 'r'
# newline = '\n'
# sip_puff_serial_port.write(request_string.encode() + newline.encode())
# Request data from sip/puff sensor.
# request_string = "r"
# sip_puff_serial_port.write(request_string.encode() + b'x0a')

# Create the menu strings
menu_string_1 = "Guitar"
newline = 'n'

while True:
	# Flush the serial input
	control_board.flushInput()
	
	# Read data from sip/puff switch.
	menu_request = control_board.readline().rstrip().decode()
	
	if(menu_request):
		print(menu_request)
	
	if(menu_request is 'g'):
		control_board.write(menu_string_1.encode() + newline.encode())
		
		
	#time.sleep(0.1)


