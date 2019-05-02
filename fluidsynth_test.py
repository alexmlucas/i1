import time
# import pyfluidsynth
import fluidsynth

fs = fluidsynth.Synth()
fs.start(driver="alsa")

# load a soundfont
try:
	sfid = fs.sfload("/usr/share/sounds/sf2/FluidR3_GM.sf2")
	# "/usr/share/sounds/sf2/FluidR3_GM.sf2"
except:
	print("could not open soundfont")
	
fs.program_select(0, sfid, 0, 0)

i = 0

while i < 5:
	
	# CC 7 is used to set channel volume.
	fs.cc(0, 7, (i * 20))
	fs.noteon(0, 60, 100)
	fs.noteon(0, 67, 100)
	fs.noteon(0, 76, 100)

	time.sleep(1.0)

	fs.noteoff(0, 60)
	fs.noteoff(0, 67)
	fs.noteoff(0, 76)

	time.sleep(1.0)
	i += 1

fs.delete()





