import time
from subprocess import call

while True:
	call("sudo mount -a", shell=True)
	time.sleep(5)
