import time
# import pyfluidsynth
import fluidsynth
import threading
#from threading import Thread
import serial

class Guitar:
	def __init__(self, guitar_tone_index, velocity, note_length):
		# intialise scales and chords
		major_pentatonic_scale = [0, 2, 4, 7, 9, 12]
		minor_pentatonic_scale = [0, 2, 3, 7, 9, 12]
		blues_scale = [0, 3, 5, 6, 7, 10]
		
		major_chord = [0, 7, 12, 16, 19, 24]
		minor_chord = [0, 7, 12, 15, 19, 24]
		
		self.transposition_offset = 40 # A standard offset to place the lowest chord in E position
		self.transposition = [0, 0, 0]
		
		self.master_note_container = [major_pentatonic_scale, minor_pentatonic_scale, blues_scale, major_chord, minor_chord]
		# create a two dimensional array of values 0
		self.zone_note_container = [[0 for i in range(6)] for i in range(3)]
		self.note_on_tracker = [None]
		
		# intialise fluidsynth
		self.fs = fluidsynth.Synth()
		self.fs.start(driver="alsa")
		
		# set the file path of each soundfont
		self.guitar_path = "/usr/share/sounds/sf2/Guitars-Universal-V1.5.sf2"
		
		# load a soundfont and initialise parameters
		self.sfid = self.fs.sfload(self.guitar_path)		
		self.velocity = velocity
		self.note_length = note_length
		
		# Intialise serial port
		self.port = '/dev/serial0'
		self.baud_rate = 9600
		self.control_board = serial.Serial(self.port, self.baud_rate, timeout = 0.1)

	def set_sound_font(self, sound_font_index):
		if sound_font_index == 0:
			# Classic Rock
			self.fs.program_select(0, self.sfid, 1, 32)
		elif sound_font_index == 1:
			# Hard Rock
			self.fs.program_select(0, self.sfid, 0, 62)
		elif sound_font_index == 2:
			# Acoustic
			self.fs.program_select(0, self.sfid, 0, 3)
		
	def set_level(self, level):
		self.fs.cc(0, 7, level)
		
	def set_zone_notes(self, zone_index, notes_index):
		# assign the scale/chord from the master note container to the zone note container 
		self.zone_note_container[zone_index] = self.master_note_container[notes_index]
		
	def set_transposition(self, zone_index, transposition_value):
		self.transposition[zone_index] = transposition_value
		
	def play_string(self, zone_index, string_index):		
		def note_event(self, note):
			print(note)
			self.tx_usb_midi_note_on_request(note)
			self.fs.noteon(0, note, self.velocity)
			time.sleep(self.note_length)
			# count if this note has only been triggered once since the note on event, send the note off message
			if self.note_on_tracker.count(note) == 1:
				self.tx_usb_midi_note_off_request(note)
				self.fs.noteoff(0, note)
			# remove the note from the tracker
			self.note_on_tracker.remove(note)
		
		# get the note to play
		note_to_play = self.zone_note_container[zone_index][string_index] + self.transposition_offset + self.transposition[zone_index]
		
		# track the note value
		self.note_on_tracker.append(note_to_play)
		
		# call note_event in a separate thread
		threading.Thread(target = note_event, args=(self, note_to_play)).start()
	
	# test serial transmission	
	def tx_usb_midi_note_on_request(self, note_number):
		character_to_transmit = 'y' + str(note_number)
		self.control_board.write(character_to_transmit.encode())
		
	def tx_usb_midi_note_off_request(self, note_number):
		character_to_transmit = 'z' + str(note_number)
		self.control_board.write(character_to_transmit.encode())
		
	def __del__(self):
		self.fs.delete()
