import pygame

class Song_Player:
	def __init__(self):
		self.song_paths = ["/boot/songs/1.wav", "/boot/songs/2.wav", "/boot/songs/3.mp3", "/boot/songs/4.mp3"]
		pygame.mixer.init()
		# A variable to track when we need to unpause rather than simply play
		self.currently_paused = False
		
	def set_song(self, song_index):
		pygame.mixer.music.load(self.song_paths[song_index])

	def set_level(self, level_as_float):
		pygame.mixer.music.set_volume(level_as_float)
		
	def set_play_state(self, play_state):
		if play_state == 0:
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


# The next function is needed to send a stop event to the device when playback has finished.
# pygame.mixer.music.set_end_event()

#while pygame.mixer.music.get_busy() == True:
	#continue
