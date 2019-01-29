# sip/puff variant
# -*- coding: utf-8 -*-
import struct
import getch
import threading
import multiprocessing
import time
from ctypes import c_bool
import serial
import rtmidi

# BT imports
import logging
import time
import uuid
import Adafruit_BluefruitLE

# Define service and characteristic UUIDs used by the BNO service.
BNO_SERVICE_UUID = uuid.UUID('369B19D1-A340-497E-A8CE-DAFA92D76793')
YAW_CHAR_UUID      = uuid.UUID('9434C16F-B011-4590-8BE3-2F97D63CC549')
MOTOR_CHAR_UUID      = uuid.UUID('14EC9994-4932-4BDA-997A-B3D052CD7421')

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

chord = 0
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# constants
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

def main():
	# BT Initialisation and connection
	# Clear any cached data because both bluez and CoreBluetooth have issues with
	# caching data and it going stale.
	ble.clear_cached_data()

	# Get the first available BLE network adapter and make sure it's powered on.
	adapter = ble.get_default_adapter()
	adapter.power_on()
	print('Using adapter: {0}'.format(adapter.name))

	# Disconnect any currently connected BNO devices.  Good for cleaning up and
	# starting from a fresh state.
	print('Disconnecting any connected BNO devices...')
	ble.disconnect_devices([BNO_SERVICE_UUID])

	# Scan for BNO devices.
	print('Searching for BNO device...')
	try:
		adapter.start_scan()
		# Search for the first BNO device found (will time out after 60 seconds
		# but you can specify an optional timeout_sec parameter to change it).
		device = ble.find_device(name='BNO')
		#device = ble.find_device(name='Adafruit Bluefruit LE')
		if device is None:
			raise RuntimeError('Failed to find BNO device!')
	finally:
		# Make sure scanning is stopped before exiting.
		adapter.stop_scan()

	print('Connecting to device...')
	device.connect()
	# Will time out after 60 seconds, specify timeout_sec parameter
	# to change the timeout.

	# Connect to serial port
	sipPuffSerialPort = serial.Serial('/dev/tty.usbmodem141111', 115200, timeout=0.1)
	# Pause to allow time for serial connection to be established.
	time.sleep(1)

	# open a MIDI port. Currently hard-wired to IAC driver.
	if available_ports:
		print(available_ports)
		midiout.open_port(1)

		# create class instances.
		myChord = ChordStrummer()

		# Intitialise variables.
		wristbandImuValueAsFloat = 0.0
		newWristbandPositionAsSegmentNumber = 0
		currentWristbandPositionAsSegmentNumber = 0

		# Flush serial inputs and outputs.
		sipPuffSerialPort.flushInput()
		sipPuffSerialPort.flushOutput()

		# Divide range of IMU into segments.
		wristbandSegmenter = StringSegmenter(-61, 0, NUMBER_OF_STRINGS)

		# flush sip puff sensor
		sipPuffSerialPort.flushInput()
		sipPuffSerialPort.flushOutput()

		# Request data from sip puff sensor.
		requestString  = 'r'
		newline = '\n'
		sipPuffSerialPort.write(requestString.encode() + newline.encode())

		# Pause between requesting and reading data.
		time.sleep(0.025)

		#######################################
		# Read data from sip/puff switch.
		newSelectedChord = sipPuffSerialPort.readline().rstrip().decode()
		currentSelectedChord = newSelectedChord
		chordToDisplay = str(currentSelectedChord)
		sipPuffSerialPort.write(chordToDisplay.encode() + b'x0a')

		try:
			# Wait for service discovery to complete for at least the specified
			# service and characteristic UUID lists.  Will time out after 60 seconds
			# (specify timeout_sec parameter to override).
			print('Discovering services...')
			device.discover([BNO_SERVICE_UUID], [YAW_CHAR_UUID, MOTOR_CHAR_UUID])

			# Find the BNO service and its characteristics.
			bno = device.find_service(BNO_SERVICE_UUID)
			yaw = bno.find_characteristic(YAW_CHAR_UUID)
			motor = bno.find_characteristic(MOTOR_CHAR_UUID)

			while True:
				# Flush serial inputs and outputs.
				sipPuffSerialPort.flushInput()
				sipPuffSerialPort.flushOutput()

				# Request data from sip/puff sensor.
				requestString  = "r"
				sipPuffSerialPort.write(requestString.encode() + b'x0a')

				# Pause between requesting and reading data.
				time.sleep(0.025)

				# Read data from sip puff sensor.
				newSelectedChord = sipPuffSerialPort.readline().rstrip().decode()

				# Read data from wristband
				wristbandImuValueAsFloat = float(yaw.read_value())

				# Convert serial strings to float values.
				#if(is_float(wristbandImuValue)):
				#wristbandImuValueAsFloat = float(wristbandImuValue)

				if (newSelectedChord != currentSelectedChord):
					chordToDisplay = str(newSelectedChord)
					sipPuffSerialPort.write(chordToDisplay.encode() + b'x0a')
					currentSelectedChord = newSelectedChord

				# this will be the code for parsing the wristband.
				newWristbandPositionAsSegmentNumber = wristbandSegmenter.determineSegment(wristbandImuValueAsFloat)

				if (newWristbandPositionAsSegmentNumber != currentWristbandPositionAsSegmentNumber):
					if (wristbandSegmenter.isSegmentAString(newWristbandPositionAsSegmentNumber)):
						print("playing notes")

						# Request that the motor be switched on here.
						motor.write_value(b'0x32\r')

						t1 = threading.Thread(target=myChord.playChord, args=(int(currentSelectedChord), wristbandSegmenter.getSegmentAsStringNumber(newWristbandPositionAsSegmentNumber)))
						t1.start()

					currentWristbandPositionAsSegmentNumber = newWristbandPositionAsSegmentNumber

				print(wristbandImuValueAsFloat)
				print(currentSelectedChord)
		finally:
			# Make sure device is disconnected on exit.
			device.disconnect()

# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
