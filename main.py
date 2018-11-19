import struct
import getch
import threading
import multiprocessing
import time
from ctypes import c_bool
import serial
import rtmidi

headsetSerialPort = serial.Serial('/dev/tty.usbmodem1411121', 115200, timeout=5)
wristbandSerialPort = serial.Serial('/dev/tty.usbmodem1411111', 115200, timeout=5)

chord = 0
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

class ReadKeyPress():
	spacebarPressed = multiprocessing.Value(c_bool, False)
	
	def spacebar(self):
		while (self.spacebarPressed.value == False):
			key = getch.getch()
			if(key == ' '):
				self.spacebarPressed.value = True
				print("spacebar press detected")

class Calibrate():
	def __init__(self, serialValue):
		self.maxValue = serialValue
		self.minValue = serialValue

	def detectMin(self, serialValue):
		if(serialValue < self.minValue):
			self.minValue = serialValue
	
	def detectMax(self, serialValue):
		if(serialValue > self.maxValue):
			self.maxValue = serialValue
			
class ChordStrummer():
	# Outputs guitar chords as MIDI notes.
	global midiout
	def playChord(self, chordNumber):
		if (chordNumber == 0):
					
			note_on = [0x90, 55, 112]
			midiout.send_message(note_on)
		
			time.sleep(0.5)
		
			note_on = [0x90, 59, 112]
			midiout.send_message(note_on)
		
			time.sleep(0.5)
		
			note_on = [0x90, 62, 112]
			midiout.send_message(note_on)
		
			time.sleep(0.5)
		
			note_off = [0x80, 55, 0]
			midiout.send_message(note_off)
			note_off = [0x80, 59, 0]
			midiout.send_message(note_off)
			note_off = [0x80, 62, 0]
			midiout.send_message(note_off)
		
class Segmenter:
	numberOfSegments = 7
	
	def __init__(self, minValue, maxValue):
		self.range = maxValue - minValue
		self.segmentSize = self.range / self.numberOfSegments
		
		self.boundaryOne = minValue
		self.boundaryTwo = minValue + self.segmentSize
		self.boundaryThree = minValue + (self.segmentSize * 2)
		self.boundaryFour = minValue + (self.segmentSize * 3)
		self.boundaryFive = minValue + (self.segmentSize * 4)
		self.boundarySix = minValue + (self.segmentSize * 5)
		self.boundarySeven = minValue + (self.segmentSize * 6)
		self.boundaryEight = maxValue
		
	def testPrintFunction(self):
		print("hello world")
	
	def printSegmentSize(self):
		print("The segment size is: ", self.segmentSize)
		
	def printBoundaries(self):
		print("The boundary values are: ")
		print(self.boundaryOne)
		print(self.boundaryTwo)
		print(self.boundaryThree)
		print(self.boundaryFour)
		print(self.boundaryFive)
		print(self.boundarySix)
		print(self.boundarySeven)
		
	def determineSegment(self, serialValue):
		# could possibly just output strings from here.
		if (serialValue >= self.boundaryOne and serialValue < self.boundaryTwo):
			return 0
			
		elif (serialValue >= self.boundaryTwo and serialValue < self.boundaryThree):
			return 1
			
		elif (serialValue >= self.boundaryThree and serialValue < self.boundaryFour):
			return 2
		
		elif (serialValue >= self.boundaryFour and serialValue < self.boundaryFive):
			return 3
		
		elif (serialValue >= self.boundaryFive and serialValue < self.boundarySix):
			return 4
		
		elif (serialValue >= self.boundarySix and serialValue < self.boundarySeven):
			return 5
		
		elif (serialValue >= self.boundarySeven and serialValue < self.boundaryEight):
			return 6

class SendCharacterString(int):
	global headsetSerialPort
	newStringToTransmit = ""
	
	def textToTransmit(self):
		print("to do")
	
	def setStringToTransmit(self, segmentNumber):
		if (segmentNumber == 0):
			self.newStringToTransmit = "1"
		elif (segmentNumber == 1):
			self.newStringToTransmit = "2"
		elif (segmentNumber == 2):
			self.newStringToTransmit = "3"
		elif (segmentNumber == 3):
			self.newStringToTransmit = "4"
		elif (segmentNumber == 4):
			self.newStringToTransmit = "5"
		elif (segmentNumber == 5):
			self.newStringToTransmit = "6"
		elif (segmentNumber == 6):
			self.newStringToTransmit = "7"
		
	def transmit(self):
		headsetSerialPort.write(self.newStringToTransmit.encode() + b'\x0a')
				
def main():
	# open a MIDI port. Currently hard-wired to IAC driver
	if available_ports:
		print(available_ports)
		midiout.open_port(1)
	
	# create class instances.
	myChord = ChordStrummer()
	updateDisplay = SendCharacterString()
	calibrationDeactivator = ReadKeyPress()
	
	# Intitialise segment position.
	currentPositionAsSegmentNumber = 0
	
	# Wait for IMU values to settle 
	for i in range (0, 20):
		print("Initialisation finishing in ", 20 - i, " seconds")
		time.sleep(1)
	
	# Read values from serial.
	headsetImuValue = headsetSerialPort.readline().rstrip().decode()
	
	if(headsetImuValue != "" and headsetImuValue != "interrupt"):
		serialValueAsFloat = float(headsetImuValue)
		
	calibration = Calibrate(serialValueAsFloat)
	p1 = multiprocessing.Process(target = calibrationDeactivator.spacebar)
	p1.start()
	
	while(calibrationDeactivator.spacebarPressed.value == False):
		
		serialValue = headsetSerialPort.readline().rstrip().decode()

		if(serialValue != "" and serialValue != "interrupt"):
			serialValueAsFloat = float(serialValue)
			print(serialValueAsFloat)
		
		calibration.detectMin(serialValueAsFloat);
		calibration.detectMax(serialValueAsFloat);
		
	print("Finished calibrating")
	print("Max value = ", calibration.maxValue)
	print("Min value = ", calibration.minValue)
	print("Entering Main Loop...")
	
	segmenter = Segmenter(calibration.minValue, calibration.maxValue)
	segmenter.printSegmentSize()
	segmenter.printBoundaries()

	print("Press any key to continue")
	key = getch.getch()
	
	while True:
		print("Main Loop...")
		
		serialValue = headsetSerialPort.readline().rstrip().decode()
		
		if(serialValue != "" and serialValue != "interrupt"):
			serialValueAsFloat = float(serialValue)
		
		newPositionAsSegmentNumber = segmenter.determineSegment(serialValueAsFloat)
		if (newPositionAsSegmentNumber != currentPositionAsSegmentNumber):
			
			t1 = threading.Thread(target=myChord.playChord, args=(newPositionAsSegmentNumber,))
			t1.start()
				
			# myChord.playChord(newPositionAsSegmentNumber)
			# update display
			updateDisplay.setStringToTransmit(newPositionAsSegmentNumber)
			updateDisplay.transmit()
			currentPositionAsSegmentNumber = newPositionAsSegmentNumber
		
if __name__ == '__main__':
	main()	

