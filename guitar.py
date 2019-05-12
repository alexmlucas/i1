import time
# import pyfluidsynth
import fluidsynth
import threading
#from threading import Thread

class Guitar:
	def __init__(self, guitar_tone_index, velocity, note_length):
		# intialise scales and chords
		major_pentatonic_scale = [0, 2, 4, 7, 9, 12]
		minor_pentatonic_scale = [0, 2, 3, 7, 9, 12]
		blues_scale = [0, 3, 5, 6, 7, 10]
		major_chord = [0, 4, 7, 12, 16, 19]
		minor_chord = [0, 3, 7, 12, 16, 18]
		self.transposition = 48
		
		self.master_note_container = [major_pentatonic_scale, minor_pentatonic_scale, blues_scale, major_chord, minor_chord]
		
		# create a two dimensional array of values 0
		self.zone_note_container = [[0 for i in range(6)] for i in range(4)]
		
		for item in self.zone_note_container:
			print(item)
		
		# intialise fluidsynth
		self.fs = fluidsynth.Synth()
		self.fs.start(driver="alsa")
		
		# set the file path of each soundfont
		self.guitar_paths = ["/usr/share/sounds/sf2/FT-EGuitarClean-20170222/FT-EGuitarClean.sfz", "/usr/share/sounds/sf2/FT-EGuitarDirect-20161019/FT-EGuitarDirect-20161019.sf2", "/usr/share/sounds/sf2/FT-EGuitarMutedClean-20161202FT-EGuitarMutedClean-20161202.sf2", "/usr/share/sounds/sf2/FluidR3_GM.sf2"]
		
		#self.guitar_paths = {"test_1", "test_2", "test_3"}
		
		# load a soundfont and initialise parameters
		sfid = self.fs.sfload(self.guitar_paths[guitar_tone_index])		
		self.velocity = velocity
		self.note_length = note_length

		# the following is perhaps not needed.
		self.fs.program_select(0, sfid, 0, 0)

	def set_guitar(self, guitar_index):
		self.fs.sfload(self.guitar_paths[guitar_index])
		
	def set_level(self, level):
		self.fs.cc(0, 7, (level * 127))
		
	def set_zone_notes(self, zone_index, notes_index):
		# assign the scale/chord from the master note container to the zone note container 
		self.zone_note_container[zone_index] = self.master_note_container[notes_index]
		
	def play_string(self, zone_index, string_index):
		
		def note_event(self, note):
			print(note)
			self.fs.noteon(0, note, self.velocity)
			time.sleep(self.note_length)
			self.fs.noteoff(0, note)
		
		# get the note to play
		note_to_play = self.zone_note_container[zone_index][string_index] + self.transposition
		# call note_event in a separate thread
		threading.Thread(target = note_event, args=(self, note_to_play)).start()
		
	def __del__(self):
		self.fs.delete()

