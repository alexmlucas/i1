import pygame

pygame.mixer.init()
pygame.mixer.music.load("/boot/songs/5.mp3")
pygame.mixer.music.load("/boot/songs/1.mp3")
# Obviously set the volume here!
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()

# Other functions needed are
# pygame.mixer.music.pause()
# pygame.mixer.music.unpause()
# pygame.mixer.music.stop()
# The next function is needed to send a stop event to the device when playback has finished.
# pygame.mixer.music.set_end_event()

while pygame.mixer.music.get_busy() == True:
	continue

