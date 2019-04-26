import serial
import time
#import io

# Connect to serial port
control_board = serial.Serial('/dev/cu.usbmodem4297351', 9600, timeout=0.1)

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

STOPPED = 0
PLAYING = 1
PAUSED = 2

playback_state = STOPPED
selected_zone = 0;

while True:
	
	
	# Read data from serial port.
	incoming_serial = control_board.readline().rstrip().decode()
	
	# Flush the serial input
	control_board.flushInput()
	
	if incoming_serial:
		print(incoming_serial)
		
	if incoming_serial == 'o1':
		print("play")
		
		if (playback_state == STOPPED or playback_state == PAUSED):
			#... switch on the play button.
			control_board.write(b'3')		# switch on the play button on the control surface.
			playback_state = PLAYING		
		elif playback_state == PLAYING:
			control_board.write(b'5')		# activate the pause state.s
			
	#control_board.write(menu_string_1.encode() + newline.encode())
		
	if incoming_serial == 'a3':
		print("song 2 requested")
		#control_board.write(menu_string_1.encode() + newline.encode())
		
	if incoming_serial == 'l0':
		if selected_zone < 2:
			selected_zone += 1
		else:
			selected_zone = 0
		
		if selected_zone == 0:
			control_board.write(b'6')
		elif selected_zone == 1:
			control_board.write(b'7')
		elif selected_zone == 2:
			control_board.write(b'8')	
		
	if incoming_serial == 'm0':
		control_board.write(b'6')
		time.sleep(3)
		control_board.write(b'8')
		
		
		
	#time.sleep(0.1)


