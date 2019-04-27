import serial
import time
import csv
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

incoming_serial = "sausages"
current_song = 0

def song_requested():
	print(current_song)
	with open('song_data.txt') as csv_file:
		song_data = csv.reader(csv_file, delimiter = ',')
		
		for row in song_data:
			print(row[current_song])
			byte_array = bytes(row[current_song], 'utf-8')
			control_board.write(byte_array)

def write_parameter(incoming_serial):
	# Indicates whether or not a parameter has been found in the list.
	write_flag = False
	# Creates a list containing 5 lists, each of 8 items, all set to 0
	w, h = 4, 9;
	song_data_as_list = [[0 for x in range(w)] for y in range(h)] 
	
	print("before data added")
	with open('song_data.txt') as csv_file:
		song_data = csv.reader(csv_file, delimiter = ',')
		
		for row in song_data:
			print(row[current_song])
	
	with open('song_data.txt') as csv_file:
		song_data_reader = csv.reader(csv_file, delimiter = ',')
		
		song_data_as_list = list(song_data_reader)
		
		index = 0
		
		for index, row in enumerate(song_data_as_list):
			cell_string = row[current_song]
			if(incoming_serial[0] == cell_string[0]):
				write_flag = True
				break
		
		if write_flag == True:
			song_data_as_list[index][current_song] = incoming_serial
		
	with open('song_data.txt', mode='w') as csv_file:
		song_data_writer = csv.writer(csv_file, delimiter = ',')
		song_data_writer.writerows(song_data_as_list)
	
	print("after data added")
	with open('song_data.txt') as csv_file:
		song_data = csv.reader(csv_file, delimiter = ',')
		
		for row in song_data:
			print(row[current_song])
			

initialisation_flag = True

while (initialisation_flag == True):
	# Read data from serial port.
	incoming_serial = control_board.readline().rstrip().decode()
	
	# Flush the serial input
	control_board.flushInput()
	
	if incoming_serial:
		print(incoming_serial)
		
		if incoming_serial[0] is 'r':
				song_requested()
		
		# Reset the flag to exit initialisation loop		
		initialisation_flag = False
	
while True:
	# Read data from serial port.
	incoming_serial = control_board.readline().rstrip().decode()
	
	# Flush the serial input
	control_board.flushInput()
	
	if incoming_serial:
		print(incoming_serial)
	
		if incoming_serial[0] is 'b':
			current_song = int(incoming_serial[2])
			song_requested()
		else:
			# add additional cases here for each parameter, play, pause, stop etc...
			write_parameter(incoming_serial)
			
	
	
	
			
	"""if incoming_serial == 'o1':
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
		
		
		
	#time.sleep(0.1)"""
	

		
	
			
	


