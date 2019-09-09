import pygame
import serial

SONG_END = pygame.USEREVENT + 1

class Song_Player:
	def __init__(self):
		self.song_paths = ["/media/usb/songs/1.wav", "/media/usb/songs/2.wav", "/media/usb/songs/3.wav", "/media/usb/songs/4.wav"]
		pygame.mixer.init()
		# A variable to track when we need to unpause rather than simply play
		self.currently_paused = False
		
		# Intialise serial port
		self.port = '/dev/serial0'
		self.baud_rate = 9600
		self.control_board = serial.Serial(self.port, self.baud_rate, timeout = 0.1)
		
		self.previous_busy_state = 0
		
	def set_song(self, song_index):
		try:
			pygame.mixer.music.load(self.song_paths[song_index])
			self.tx_song_loaded_status(True)
		except:
			# The song could not be loaded.
			self.tx_song_loaded_status(False)
		

	def set_level(self, level_as_float):
		pygame.mixer.music.set_volume(level_as_float)
		
	def set_play_state(self, play_state):
		if play_state == 0:
			if self.currently_paused == True:
				pygame.mixer.music.unpause()
				self.currently_paused = False
			pygame.mixer.music.stop()
		elif play_state == 1:
			if self.currently_paused == True:
				pygame.mixer.music.unpause()
				self.currently_paused = False
			else:
				pygame.mixer.music.play()
		elif play_state == 2:
			pygame.mixer.music.pause()
			self.currently_paused = True
		
				
	def tx_song_loaded_status(self, status):
		if status == True:
			characters_to_transmit = 't01'
		else:
			characters_to_transmit = 't00'
		
		self.control_board.write(characters_to_transmit.encode())
		
	def check_song_end(self):
		# Update the transport on the control board when a song stops playing.
		current_busy_state = pygame.mixer.music.get_busy()
		
		if current_busy_state is not self.previous_busy_state:
			if current_busy_state == 0:
				self.tx_stop()
			self.previous_busy_state = current_busy_state
			
	def tx_stop(self):
		# update the transport to a stopped state on the control board
		characters_to_transmit = 'o00'
		self.control_board.write(characters_to_transmit.encode())
		
	
# The next function is needed to send a stop event to the device when playback has finished.
# pygame.mixer.music.set_end_event()

#while pygame.mixer.music.get_busy() == True:
	#continue
