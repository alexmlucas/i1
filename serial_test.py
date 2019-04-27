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

def write_song_parameter(incoming_serial):
	# Indicates whether or not a parameter has been found in the list.
	write_flag = False
	# Creates a list containing 5 lists, each of 8 items, all set to 0
	w, h = 4, 9;
	song_data_as_list = [[0 for x in range(w)] for y in range(h)] 
	
	'''print("before data added")
	with open('song_data.txt') as csv_file:
		song_data = csv.reader(csv_file, delimiter = ',')
		
		for row in song_data:
			print(row[current_song])'''
	
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
	
	'''print("after data added")
	with open('song_data.txt') as csv_file:
		song_data = csv.reader(csv_file, delimiter = ',')
		
		for row in song_data:
			print(row[current_song])'''

def write_global_parameter(incoming_serial):
	# Indicates whether or not a parameter has been found in the list.
	write_flag = False
	# Creates a list containing 5 lists, each of 8 items, all set to 0
	w, h = 2, 1;
	global_data_as_list = [[0 for x in range(w)] for y in range(h)] 
	
	'''print("before data added")
	with open('global_data.txt') as csv_file:
		global_data_reader = csv.reader(csv_file, delimiter = ',')
		global_data_as_list = list(global_data_reader)
		print(global_data_as_list)'''
	
	with open('global_data.txt') as csv_file:
		global_data_reader = csv.reader(csv_file, delimiter = ',')
		
		global_data_as_list = list(global_data_reader)
		
		row_index = 0
		cell_index = 0
		
		for row_index, row in enumerate(global_data_as_list):
			
			for cell_index, cell_string in enumerate(row):
				if(incoming_serial[0] == cell_string[0]):
					write_flag = True
					break
					
			if(write_flag == True):
				break
		
		if write_flag == True:
			global_data_as_list[row_index][cell_index] = incoming_serial
		
	with open('global_data.txt', mode='w') as csv_file:
		global_data_writer = csv.writer(csv_file, delimiter = ',')
		global_data_writer.writerows(global_data_as_list)
	
	'''print("after data added")
	with open('global_data.txt') as csv_file:
		global_data_reader = csv.reader(csv_file, delimiter = ',')
		global_data_as_list = list(global_data_reader)
		print(global_data_as_list)'''
	

# *** Parameter Functions ***

def set_master_level(incoming_serial):
	# Slice the string to remove the first character and convert to int
	master_level = int(incoming_serial[1:])
	print('Master Level = ', master_level)

def set_guitar(incoming_serial):
	# Slice the string to remove the first character and convert to int
	guitar = int(incoming_serial[1:])
	print('Guitar = ', guitar)

def set_guitar_level(incoming_serial):
	# Slice the string to remove the first character and convert to int
	guitar_level = int(incoming_serial[1:])
	print('Guitar Level = ', guitar_level)

def set_backing_level(incoming_serial):
	# Slice the string to remove the first character and convert to int
	backing_level = int(incoming_serial[1:])
	print('Backing Level = ', backing_level)

def set_red_scale(incoming_serial):
	# Slice the string to remove the first character and convert to int
	red_scale = int(incoming_serial[1:])
	print('Red Scale = ', red_scale)

def set_green_scale(incoming_serial):
	# Slice the string to remove the first character and convert to int
	green_scale = int(incoming_serial[1:])
	print('Green Scale = ', green_scale)

def set_blue_scale(incoming_serial):
	# Slice the string to remove the first character and convert to int
	blue_scale = int(incoming_serial[1:])
	print('Blue Scale = ', blue_scale)

def set_red_root(incoming_serial):
	# Slice the string to remove the first character and convert to int
	red_root = int(incoming_serial[1:])
	print('Red Root = ', red_root)

def set_blue_root(incoming_serial):
	# Slice the string to remove the first character and convert to int
	blue_root = int(incoming_serial[1:])
	print('Blue Root = ', blue_root)
	
def set_green_root(incoming_serial):
	# Slice the string to remove the first character and convert to int
	blue_root = int(incoming_serial[1:])
	print('Green Root = ', blue_root)

def set_zone(incoming_serial):
	# Slice the string to remove the first character and convert to int
	zone = int(incoming_serial[1:])
	print('Zone = ', zone)
	
def reconnect_wristband(incoming_serial):
	print('Reconnecting to wristband')
	
def shutdown_device(incoming_serial):
	print('Shutting down')
	
def set_playback_state(incoming_serial):
	# Slice the string to remove the first character and convert to int
	playback_state = int(incoming_serial[1:])
	print('Playback State = ', playback_state)
	

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
		#print(incoming_serial)
	
		if incoming_serial[0] is 'a':
			# Master level (Global Parameter)
			# Local action
			set_master_level(incoming_serial)
			# Write the parameter
			write_global_parameter(incoming_serial)
			
		elif incoming_serial[0] is 'b':
			# Song (Global Parameter)
			# Local action
			current_song = int(incoming_serial[2])
			# Write the parameter
			write_global_parameter(incoming_serial)
			song_requested()
			
		elif incoming_serial[0] is 'c':
			# Guitar
			# Local action
			set_guitar(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)
			
		elif incoming_serial[0] is 'd':
			# Guitar Level
			# Local action
			set_guitar_level(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)
			
		elif incoming_serial[0] is 'e':
			# Backing Level
			# Local action
			set_backing_level(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)	
			
		elif incoming_serial[0] is 'f':
			# Red Scale
			# Local action
			set_red_scale(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)	
				
		elif incoming_serial[0] is 'g':
			# Green Scale
			# Local action
			set_green_scale(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)		
			
		elif incoming_serial[0] is 'h':
			# Blue Scale
			# Local action
			set_blue_scale(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)	
		
		elif incoming_serial[0] is 'i':
			# Red Root
			# Local action
			set_red_root(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)	
		
		elif incoming_serial[0] is 'j':
			# Blue Root
			# Local action
			set_blue_root(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)	
			
		elif incoming_serial[0] is 'k':
			# Green Root
			# Local action
			set_green_root(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)	
		
		elif incoming_serial[0] is 'l':
			# Zone
			# Local action
			set_zone(incoming_serial)
			# Write the parameter
			write_song_parameter(incoming_serial)	
		
		elif incoming_serial[0] is 'm':
			# Reconnect Request
			# Local action
			reconnect_wristband(incoming_serial)
		
		elif incoming_serial[0] is 'n':
			# Power
			# Local action
			shutdown_device(incoming_serial)

		elif incoming_serial[0] is 'o':
			# Play
			# Local action
			set_playback_state(incoming_serial)
			
	
	
	
			
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
	

		

			
	


