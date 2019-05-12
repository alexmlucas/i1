import serial
import csv

class Parameter_Manager:

	def __init__(self, port, baud_rate):
		self.port = port
		self.baud_rate = baud_rate
		
		# current song - does this need to be loaded from the song_data text file?
		self.current_song = self.get_last_selected_song()
		
		# Intialise serial port
		self.control_board = serial.Serial(self.port, self.baud_rate, timeout = 0.1)
		
		# Flush inputs and outputs
		self.control_board.flushInput()
		self.control_board.flushOutput()
		
	# def intialise_parameters
	
	def check_incoming(self):
		# Read data from the serial port
		incoming_serial = self.control_board.readline().rstrip().decode()
		
		# Flush the serial port
		self.control_board.flushInput()
		
		if incoming_serial:
			print(incoming_serial)
			print(self.current_song)
			
			if incoming_serial[0] is 'a':
				# Master level (Global Parameter)
				# Local action
				self.set_master_level(incoming_serial)
				# Write the parameter
				self.write_global_parameter(incoming_serial)
				
			elif incoming_serial[0] is 'b':
				# Song (Global Parameter)
				# Local action
				self.current_song = int(incoming_serial[2])
				# Write the parameter
				self.write_global_parameter(incoming_serial)
				self.song_data_requested()
				
			elif incoming_serial[0] is 'c':
				# Guitar
				# Local action
				self.set_guitar(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)
				
			elif incoming_serial[0] is 'd':
				# Guitar Level
				# Local action
				self.set_guitar_level(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)
				
			elif incoming_serial[0] is 'e':
				# Backing Level
				# Local action
				self.set_backing_level(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)	
				
			elif incoming_serial[0] is 'f':
				# Red Scale
				# Local action
				self.set_red_scale(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)	
					
			elif incoming_serial[0] is 'g':
				# Green Scale
				# Local action
				self.set_green_scale(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)		
				
			elif incoming_serial[0] is 'h':
				# Blue Scale
				# Local action
				self.set_blue_scale(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)	
			
			elif incoming_serial[0] is 'i':
				# Red Root
				# Local action
				self.set_red_root(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)	
			
			elif incoming_serial[0] is 'j':
				# Blue Root
				# Local action
				self.set_blue_root(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)	
				
			elif incoming_serial[0] is 'k':
				# Green Root
				# Local action
				self.set_green_root(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)	
			
			elif incoming_serial[0] is 'l':
				# Zone
				# Local action
				self.set_zone(incoming_serial)
				# Write the parameter
				self.write_song_parameter(incoming_serial)	
			
			elif incoming_serial[0] is 'm':
				# Reconnect Request
				# Local action
				self.reconnect_wristband(incoming_serial)
			
			elif incoming_serial[0] is 'n':
				# Power
				# Local action
				self.shutdown_device(incoming_serial)

			elif incoming_serial[0] is 'o':
				# Play
				# Local action
				self.set_playback_state(incoming_serial)
				
			elif incoming_serial[0] is 'r':
				# Initial data request.
				# Send the global parameters
				self.global_data_requested()
				
				# Send the song data
				self.song_data_requested()
				
				
	def set_master_level(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		master_level = int(incoming_serial[1:])
		print('Master Level = ', master_level)

	def set_guitar(self,incoming_serial):
		# Slice the string to remove the first character and convert to int
		guitar = int(incoming_serial[1:])
		print('Guitar = ', guitar)

	def set_guitar_level(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		guitar_level = int(incoming_serial[1:])
		print('Guitar Level = ', guitar_level)

	def set_backing_level(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		backing_level = int(incoming_serial[1:])
		print('Backing Level = ', backing_level)

	def set_red_scale(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		red_scale = int(incoming_serial[1:])
		print('Red Scale = ', red_scale)

	def set_green_scale(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		green_scale = int(incoming_serial[1:])
		print('Green Scale = ', green_scale)

	def set_blue_scale(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		blue_scale = int(incoming_serial[1:])
		print('Blue Scale = ', blue_scale)

	def set_red_root(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		red_root = int(incoming_serial[1:])
		print('Red Root = ', red_root)

	def set_blue_root(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		blue_root = int(incoming_serial[1:])
		print('Blue Root = ', blue_root)
		
	def set_green_root(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		blue_root = int(incoming_serial[1:])
		print('Green Root = ', blue_root)

	def set_zone(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		zone = int(incoming_serial[1:])
		print('Zone = ', zone)
		
	def reconnect_wristband(self, incoming_serial):
		print('Reconnecting to wristband')
		
	def wristband_connection_failure(self):
		print('Cannot connect')
		# Send serial message here.
		
	def shutdown_device(self, incoming_serial):
		print('Shutting down')
		
	def set_playback_state(self, incoming_serial):
		# Slice the string to remove the first character and convert to int
		playback_state = int(incoming_serial[1:])
		print('Playback State = ', playback_state)
		
	def write_song_parameter(self, incoming_serial):
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
			# Convert the song data to a list so that we can easily work with it.
			song_data_as_list = list(song_data_reader)
			
			# Initialise an index variable for use with the following for loop
			index = 0
			
			# Interate through the song data list 
			for index, row in enumerate(song_data_as_list):
				# Isolate the parameter associated with the currently selected song
				cell_string = row[self.current_song]
				
				# If the first character matches that of the incoming serial...
				if(incoming_serial[0] == cell_string[0]):
					#... indicate that we need to overwrite the parameter in this position.
					write_flag = True
					break
			
			# If the write flag is true...
			if write_flag == True:
				#... overwrite the parameter in the array.
				song_data_as_list[index][self.current_song] = incoming_serial
			
				# and write the data to the song data text file.
				with open('song_data.txt', mode='w') as csv_file:
					song_data_writer = csv.writer(csv_file, delimiter = ',')
					song_data_writer.writerows(song_data_as_list)
			
		'''print("after data added")
		with open('song_data.txt') as csv_file:
			song_data = csv.reader(csv_file, delimiter = ',')
			
			for row in song_data:
				print(row[current_song])'''

	def write_global_parameter(self, incoming_serial):
		# Indicates whether or not a parameter has been found in the list.
		write_flag = False
		# Create a 2 x 1 array, initialised to 0
		w, h = 2, 1;
		global_data_as_list = [[0 for x in range(w)] for y in range(h)] 
		
		'''print("before data added")
		with open('global_data.txt') as csv_file:
			global_data_reader = csv.reader(csv_file, delimiter = ',')
			global_data_as_list = list(global_data_reader)
			print(global_data_as_list)'''
		
		with open('global_data.txt') as csv_file:
			global_data_reader = csv.reader(csv_file, delimiter = ',')
			# Convert the global data to a list so that we can easily work with it.
			global_data_as_list = list(global_data_reader)
			
			# initialise index's for iterating through the following for loop.
			row_index = 0
			cell_index = 0
			
			for row_index, row in enumerate(global_data_as_list):
				
				for cell_index, cell_string in enumerate(row):
					# If the first character matches that of the incoming serial...
					if(incoming_serial[0] == cell_string[0]):
						#... indicate that we need to overwrite the parameter in this position.
						write_flag = True
						break
				
				# Exit the parent for loop
				if(write_flag == True):
					break
			
			# If the write flag is true...
			if write_flag == True:
				#... overwrite the parameter in the array.
				global_data_as_list[row_index][cell_index] = incoming_serial
				
			# and write the data to the song data text file.	
			with open('global_data.txt', mode='w') as csv_file:
				global_data_writer = csv.writer(csv_file, delimiter = ',')
				global_data_writer.writerows(global_data_as_list)
			
			'''print("after data added")
			with open('global_data.txt') as csv_file:
				global_data_reader = csv.reader(csv_file, delimiter = ',')
				global_data_as_list = list(global_data_reader)
				print(global_data_as_list)'''
	
	def global_data_requested(self):
		with open('global_data.txt') as csv_file:
			global_data = csv.reader(csv_file, delimiter = ',')
			
			# Nasty hack to get global data sent.
			# Will need to be changed if more data is added to the text file
			for row in global_data:
				byte_array = bytes(row[0], 'utf-8')
				self.control_board.write(byte_array)
				
				byte_array = bytes(row[1], 'utf-8')
				self.control_board.write(byte_array)
	
	
	
	def song_data_requested(self):
		with open('song_data.txt') as csv_file:
			song_data = csv.reader(csv_file, delimiter = ',')
			
			for row in song_data:
				byte_array = bytes(row[self.current_song], 'utf-8')
				print(byte_array)
				self.control_board.write(byte_array)
				
	def get_last_selected_song(self):
		# create a 2 x 1 array
		w, h = 2, 1;
		global_data_as_list = [[0 for x in range(w)] for y in range(h)] 
	
		with open('global_data.txt') as csv_file:
			global_data_reader = csv.reader(csv_file, delimiter = ',')
			
			global_data_as_list = list(global_data_reader)
			
			row_index = 0
			cell_index = 0
			
			for row_index, row in enumerate(global_data_as_list):
				for cell_index, cell_string in enumerate(row):
					if(cell_string[0] == 'b'):
						# song parameter found
						return int(cell_string[2])
	
	def get_global_parameter(self, parameter_character):
		# create a 2 x 1 array
		w, h = 2, 1;
		global_data_as_list = [[0 for x in range(w)] for y in range(h)] 
	
		with open('global_data.txt') as csv_file:
			global_data_reader = csv.reader(csv_file, delimiter = ',')
			
			global_data_as_list = list(global_data_reader)
			
			row_index = 0
			cell_index = 0
			
			for row_index, row in enumerate(global_data_as_list):
				for cell_index, cell_string in enumerate(row):
					# If the first character matches...
					if(parameter_character == cell_string[0]):
						#... return the value
						return int(cell_string[2]) + (int(cell_string[1]) * 10)
						
	def get_song_parameter(self, parameter_character):
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
			# Convert the song data to a list so that we can easily work with it.
			song_data_as_list = list(song_data_reader)
			
			# Initialise an index variable for use with the following for loop
			index = 0
			
			# Interate through the song data list 
			for index, row in enumerate(song_data_as_list):
				# Isolate the parameter associated with the currently selected song
				cell_string = row[self.current_song]
				
				# If the first character matches...
				if(parameter_character == cell_string[0]):
					#... return the value
					return int(cell_string[2]) + (int(cell_string[1]) * 10)
	
