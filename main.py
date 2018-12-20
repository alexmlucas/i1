import struct
import getch
import threading
import multiprocessing
import time
from ctypes import c_bool
import serial
import rtmidi

chord = 0
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# Constants
NUMBER_OF_CHORDS = 2
NUMBER_OF_STRINGS = 6

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
	global midiout
	cMajorChordMidiNoteValues = [[0, 48, 52, 55, 60, 64],[0, 0, 50, 57, 62, 65],[40, 47, 52, 55, 59, 64],[0, 0, 53, 55, 60, 65],[43, 47, 50, 55, 59, 65],[0, 45, 52, 57, 60, 64],[0, 47, 50, 55, 62, 0]]
	
	def playChord(self, chordNumber, stringNumber):
		if (self.cMajorChordMidiNoteValues[chordNumber][stringNumber] != 0):
			note_on = [0x90, self.cMajorChordMidiNoteValues[chordNumber][stringNumber], 112]
			midiout.send_message(note_on)
			time.sleep(0.5)
			note_off = [0x80, self.cMajorChordMidiNoteValues[chordNumber][stringNumber], 0]
			midiout.send_message(note_off)


class ChordSegmenter():
	def __init__(self, minValue, maxValue, numberOfChords):
		self.minValue = minValue
		self.maxValue = maxValue
		self.numberOfSegments = numberOfChords
		self.range = maxValue - minValue
		self.segmentSize = self.range / self.numberOfSegments
		self.segmentBoundaries = []
		self.currentlySelectedSegment = 0
				
		index = 0
		while (index <= self.numberOfSegments):
			self.segmentBoundaries.append(self.minValue + (self.segmentSize * (index)))
			index += 1
		
	def getSegmentSize(self):
		return self.segmentSize
		
	def getBoundaries(self):
		return self.segmentBoundaries
				
	def determineSegment(self, serialValue):
		for index, boundaryValue in enumerate(self.segmentBoundaries):
			if (serialValue > boundaryValue):
				# Update index and continue to iterate through boundary values
				self.currentlySelectedSegment = index;
			else:
				break
		
		return self.currentlySelectedSegment

class StringSegmenter():
	def __init__(self, minValue, maxValue, numberOfStrings):
		self.minValue = minValue
		self.maxValue = maxValue
		# The number of segments needs to be twice the number of strings (+ 1) to allow for dead space.
		self.numberOfSegments = (numberOfStrings * 2) + 1
		self.range = maxValue - minValue
		self.segmentSize = self.range / self.numberOfSegments
		self.segmentBoundaries = []
		self.currentlySelectedSegment = 0
				
		index = 0
		while (index <= self.numberOfSegments):
			self.segmentBoundaries.append(self.minValue + (self.segmentSize * (index)))
			index += 1
		
		
	def getSegmentAsStringNumber(self, segment):
		stringNumber = (segment / 2) - 0.5
		return int(stringNumber)
	
	def getSegmentSize(self):
		return self.segmentSize
		
	def getBoundaries(self):
		return self.segmentBoundaries
				
	def determineSegment(self, serialValue):
		for index, boundaryValue in enumerate(self.segmentBoundaries):
			if (serialValue > boundaryValue):
				# Update index and continue to iterate through boundary values
				self.currentlySelectedSegment = index;
			else:
				break
		
		return self.currentlySelectedSegment
		
	def isSegmentAString(self, segment):
		if segment <= 12 and segment >= 0 and segment % 2 > 0:
			return True
		else:
			return False

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
		 
def is_float(value):
  try:
    float(value)  
    return True
  except:
    return False
				
def main():
	# Connect to serial ports
	headsetSerialPort = serial.Serial('/dev/tty.usbmodem143141', 115200, timeout=0.1)
	wristbandSerialPort = serial.Serial('/dev/tty.usbmodem143131', 115200, timeout=0.1)
	
	# Pause to allow time for serial connection to be established.
	time.sleep(1)
	
	# open a MIDI port. Currently hard-wired to IAC driver.
	if available_ports:
		print(available_ports)
		midiout.open_port(1)
	
	# create class instances.
	myChord = ChordStrummer()
	updateDisplay = SendCharacterString()
	calibrationDeactivator = ReadKeyPress()
	
	# Intitialise variables.
	headsetImuValueAsFloat = 0.0
	wristbandImuValueAsFloat = 0.0
	newHeadsetPositionAsSegmentNumber = 0
	currentHeadsetPositionAsSegmentNumber = 0
	newWristbandPositionAsSegmentNumber = 0
	currentWristbandPositionAsSegmentNumber = 0
	
	# Wait for IMU values to settle.
	for i in range (0, 20):
		print("Initialisation finishing in ", 20 - i, " seconds")
		time.sleep(1)
		
	# Flush serial inputs and outputs.
	headsetSerialPort.flushInput()
	headsetSerialPort.flushOutput()
	wristbandSerialPort.flushInput()
	wristbandSerialPort.flushOutput()
	
	# Request data from headset and wristband.
	requestString  = "r"
	headsetSerialPort.write(requestString.encode() + b'x0a')
	wristbandSerialPort.write(requestString.encode() + b'x0a')
	
	# Pause between requesting and reading data.
	time.sleep(0.025)
	
	# Read data from headset and wristband.
	headsetImuValue = headsetSerialPort.readline().rstrip().decode()
	wristbandImuValue = wristbandSerialPort.readline().rstrip().decode()
	
	# Convert serial strings to float values.
	if(is_float(headsetImuValue)):
		headsetImuValueAsFloat = float(headsetImuValue)
				
	if(is_float(wristbandImuValue)):
		wristbandImuValueAsFloat = float(wristbandImuValue)
	
	# Create an instance of calibration classes for IMU's.
	headsetImuCalibration = Calibrate(headsetImuValueAsFloat)
	wristbandImuCalibration = Calibrate(wristbandImuValueAsFloat)
	
	# Start a separate process to detect a spacebar press.
	p1 = multiprocessing.Process(target = calibrationDeactivator.spacebar)
	p1.start()
	
	# Prior to a spacebar press being detected set min and max values for each IMU
	while(calibrationDeactivator.spacebarPressed.value == False):
		# Flush serial inputs and outputs.
		headsetSerialPort.flushInput()
		headsetSerialPort.flushOutput()
		wristbandSerialPort.flushInput()
		wristbandSerialPort.flushOutput()
		
		# Request data from headset and wristband.
		requestString  = "r"
		headsetSerialPort.write(requestString.encode() + b'x0a')
		wristbandSerialPort.write(requestString.encode() + b'x0a')
		
		# Pause between requesting and reading data.
		time.sleep(0.025)
	
		# Read data from headset and wristband.
		headsetImuValue = headsetSerialPort.readline().rstrip().decode()
		wristbandImuValue = wristbandSerialPort.readline().rstrip().decode()
		
		# Convert serial strings to float values.
		if(is_float(headsetImuValue)):
			headsetImuValueAsFloat = float(headsetImuValue)
				
		if(is_float(wristbandImuValue)):
			wristbandImuValueAsFloat = float(wristbandImuValue)
		
		print(headsetImuValueAsFloat, '\t', wristbandImuValueAsFloat)
		
		# Set headset IMU min and max values.
		headsetImuCalibration.detectMin(headsetImuValueAsFloat);
		headsetImuCalibration.detectMax(headsetImuValueAsFloat);
		
		# Set wristband IMU min and max values.
		wristbandImuCalibration.detectMin(wristbandImuValueAsFloat);
		wristbandImuCalibration.detectMax(wristbandImuValueAsFloat);
		
	print("Finished calibrating")
	
	print("")
	
	# Print values to terminal for debugging purposes.
	print("Headset IMU max value = ", headsetImuCalibration.maxValue)
	print("Headset IMU min value = ", headsetImuCalibration.minValue)
	print("Wristband IMU max value = ", wristbandImuCalibration.maxValue)
	print("Wristband IMU min value = ", wristbandImuCalibration.minValue)
	
	print("")
	
	print("Entering Main Loop...")
	
	# Divide range of IMU's into segments.
	headsetSegmenter = ChordSegmenter(headsetImuCalibration.minValue, headsetImuCalibration.maxValue, NUMBER_OF_CHORDS)
	wristbandSegmenter = StringSegmenter(wristbandImuCalibration.minValue, wristbandImuCalibration.maxValue, NUMBER_OF_STRINGS)
	
	print("Headset Values")
	print("--------------")
	print("Segment Size: ", headsetSegmenter.getSegmentSize())
	print("Boundary Values: ")
	for boundaryValue in headsetSegmenter.getBoundaries():
		print(boundaryValue)
	print("")
	
	print("Wristband Values")
	print("----------------")
	print("Segment Size: ", wristbandSegmenter.getSegmentSize())
	print("Boundary Values: ")
	for boundaryValue in wristbandSegmenter.getBoundaries():
		print(boundaryValue)
	print("")
	
	print("Press any key to continue")
	key = getch.getch()
	
	print("Starting main loop...")
	
	# Set initial LED state.
	newHeadsetPositionAsSegmentNumber = headsetSegmenter.determineSegment(headsetImuValueAsFloat)
	characterToDisplay = str(newHeadsetPositionAsSegmentNumber + 1)
	headsetSerialPort.write(characterToDisplay.encode() + b'x0a')
	currentHeadsetPositionAsSegmentNumber = newHeadsetPositionAsSegmentNumber 
	
	while True:
		# Flush serial inputs and outputs.
		headsetSerialPort.flushInput()
		headsetSerialPort.flushOutput()
		wristbandSerialPort.flushInput()
		wristbandSerialPort.flushOutput()
	
		# Request data from headset and wristband.
		requestString  = "r"
		headsetSerialPort.write(requestString.encode() + b'x0a')
		wristbandSerialPort.write(requestString.encode() + b'x0a')
	
		# Pause between requesting and reading data.
		time.sleep(0.025)
	
		# Read data from headset and wristband.
		headsetImuValue = headsetSerialPort.readline().rstrip().decode()
		wristbandImuValue = wristbandSerialPort.readline().rstrip().decode()
	
		# Convert serial strings to float values.
		if(is_float(headsetImuValue)):
			headsetImuValueAsFloat = float(headsetImuValue)
				
		if(is_float(wristbandImuValue)):
			wristbandImuValueAsFloat = float(wristbandImuValue)
		
		newHeadsetPositionAsSegmentNumber = headsetSegmenter.determineSegment(headsetImuValueAsFloat)
		
		if (newHeadsetPositionAsSegmentNumber != currentHeadsetPositionAsSegmentNumber):	
			characterToDisplay = str(newHeadsetPositionAsSegmentNumber + 1)
			headsetSerialPort.write(characterToDisplay.encode() + b'x0a')
			currentHeadsetPositionAsSegmentNumber = newHeadsetPositionAsSegmentNumber 
		
		# this will be the code for parsing the wristband.
		newWristbandPositionAsSegmentNumber = wristbandSegmenter.determineSegment(wristbandImuValueAsFloat)
		
		if (newWristbandPositionAsSegmentNumber != currentWristbandPositionAsSegmentNumber):
			if (wristbandSegmenter.isSegmentAString(newWristbandPositionAsSegmentNumber)):
				print("playing notes")
				t1 = threading.Thread(target=myChord.playChord, args=(currentHeadsetPositionAsSegmentNumber, wristbandSegmenter.getSegmentAsStringNumber(newWristbandPositionAsSegmentNumber)))
				t1.start()
			
			currentWristbandPositionAsSegmentNumber = newWristbandPositionAsSegmentNumber
		
		print(headsetImuValueAsFloat, '\t', wristbandImuValueAsFloat)
		print(currentHeadsetPositionAsSegmentNumber, "\t", currentWristbandPositionAsSegmentNumber)	
		

if __name__ == '__main__':
	main()	

