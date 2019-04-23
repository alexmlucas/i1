# sip/puff variant
# -*- coding: utf-8 -*-

# what are abstract methods and properties?
import struct
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
# from Adafruit_BluefruitLE.services import UART

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



class ChordStrummer:
	c_major_chord_notes = [[0, 48, 52, 55, 60, 64],[0, 0, 50, 57, 62, 65],[40, 47, 52, 55, 59, 64],[0, 0, 53, 55, 60, 65],[43, 47, 50, 55, 59, 65],[0, 45, 52, 57, 60, 64],[0, 47, 50, 55, 62, 0]]

	def play_chord(self, chord_number, string_number):
		# print(f"chord #: {chord_number}, string_number {string_number} ")
		if self.c_major_chord_notes[chord_number][string_number] != 0:
			note_on = [0x90, self.c_major_chord_notes[chord_number][string_number], 112]
			midiout.send_message(note_on)
			time.sleep(0.5)
			note_off = [0x80, self.c_major_chord_notes[chord_number][string_number], 0]
			midiout.send_message(note_off)


class StringSegmenter:
	def __init__(self, min_value, max_value, number_of_strings):
		self.min_value = min_value
		self.max_value = max_value
		# The number of segments needs to be twice the number of strings (+ 1) to allow for dead space.
		self.number_of_segments = (number_of_strings * 2) + 1
		self.range = max_value - min_value
		self.segment_size = self.range / self.number_of_segments
		self.segment_boundaries = []
		self.currently_selected_segment = 0

		index = 0
		while index <= self.number_of_segments:
			self.segment_boundaries.append(self.min_value + (self.segment_size * (index)))
			index += 1

	def get_segment_as_string_number(self, segment):
		string_number = (segment / 2) - 0.5
		return int(string_number)

	def get_segment_size(self):
		return self.segment_size

	def get_boundaries(self):
		return self.segment_boundaries

	def determine_segment(self, serial_value):
		for index, boundary_value in enumerate(self.segment_boundaries):
			if serial_value > boundary_value:
				# Update index and continue to iterate through boundary values
				self.currently_selected_segment = index
			else:
				break

		return self.currently_selected_segment

	def is_segment_a_string(self, segment):
		if segment <= 12 and segment >= 0 and segment % 2 > 0:
			return True
		else:
			return False


# https://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread

class ChordStrummerThread(threading.Thread):
	# Thread class with a stop() method. The thread itself has to check
	# regularly for the stopped() condition.
	# https: // www.pythoncentral.io/how-to-create-a-thread-in-python/
	# https: // www.youtube.com / watch?v = cY9pih5Sdk4
	c_major_chord_notes = [[0, 48, 52, 55, 60, 64], [0, 0, 50, 57, 62, 65], [40, 47, 52, 55, 59, 64], [0, 0, 53, 55, 60, 65], [43, 47, 50, 55, 59, 65], [0, 45, 52, 57, 60, 64], [0, 47, 50, 55, 62, 0]]

	def __init__(self, chord, string):
		super(ChordStrummerThread, self).__init__()
		# https://docs.python.org/2.0/lib/event-objects.html
		self._stop_event = threading.Event()
		self.chord_number = chord
		self.string_number = string

	def stop(self):
		# sets the stop event to true.
		self._stop_event.set()

	def stopped(self):
		return self._stop_event.is_set

	def run(self):
		if self.c_major_chord_notes[self.chord_number][self.string_number] != 0:
			note_on = [0x90, self.c_major_chord_notes[self.chord_number][self.string_number], 112]
			midiout.send_message(note_on)
			time.sleep(0.5)
			note_off = [0x80, self.c_major_chord_notes[self.chord_number][self.string_number], 0]
			midiout.send_message(note_off)
			self._stop_event.set()


def main():

	my_chord = ChordStrummer()
	note_events = []

	loom = []

	def trigger_thread(guitar_string_number):
		t1 = threading.Thread(target=my_chord.play_chord, args=(int(current_selected_chord), guitar_string_number))
		loom.append(t1)
		t1.start()

	def is_float(value):
		try:
			float(value)
			return True
		except ValueError:
			return False

	def received(data):
		if is_float(data):
			float_data = float(data)
			print(float_data)
			int_data = int(float_data)
			if int_data is not -1:
				# chord is triggered here...
				n1 = ChordStrummerThread(int(current_selected_chord), int(float_data))
				note_events.append(n1)
				n1.start()

				#trigger_thread(int(float_data))

	current_selected_chord = 1

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
	print('Disconnecting any connected UART devices...')
	ble.disconnect_devices([BNO_SERVICE_UUID])
	##UART.disconnect_devices()

	# Scan for BNO devices.tony d bluetooth raspberry pi

	print('Searching for BNO device...')
	try:
		adapter.start_scan()
		# Search for the first BNO device found (will time out after 60 seconds
		# but you can specify an optional timeout_sec parameter to change it).
		#device = ble.find_device(name='BNO')
		device = ble.find_device(service_uuids=[BNO_SERVICE_UUID])

		# device = ble.find_device(name='Adafruit Bluefruit LE')

		## device = UART.find_device()

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
	sip_puff_serial_port = serial.Serial('/dev/tty.usbmodem141141', 115200, timeout=0.1)
	# Pause to allow time for serial connection to be established.
	time.sleep(1)

	# open a MIDI port. Currently hard-wired to IAC driver.
	if available_ports:
		print(available_ports)
		# midiout.open_port(1)

		# Intitialise variables.
		wristband_imu_value_as_float = 0.0
		new_wristband_position_as_segment_number = 0
		current_wristband_position_as_segment_number = 0

		# Flush serial inputs and outputs.
		## sip_puff_serial_port.flushInput()
		## sip_puff_serial_port.flushOutput()

		# Divide range of IMU into segments.
		wristband_segmenter = StringSegmenter(-61, 0, NUMBER_OF_STRINGS)

		# flush sip puff sensor
		## sip_puff_serial_port.flushInput()
		## sip_puff_serial_port.flushOutput()

		# Request data from sip puff sensor.
		request_string  = 'r'
		newline = '\n'
		## sip_puff_serial_port.write(request_string.encode() + newline.encode())

		# Pause between requesting and reading data.
		time.sleep(0.025)

		#######################################
		# Read data from sip/puff switch.
		# new_selected_chord = sip_puff_serial_port.readline().rstrip().decode()
		## current_selected_chord = new_selected_chord

		current_selected_chord = 1
		chord_to_display = str(current_selected_chord)
		## sip_puff_serial_port.write(chord_to_display.encode() + b'x0a')
		pluck_time = None

		try:
			# Wait for service discovery to complete for at least the specified
			# service and characteristic UUID lists.  Will time out after 60 seconds
			# (specify timeout_sec parameter to override).
			print('Discovering services...')
			device.discover([BNO_SERVICE_UUID], [YAW_CHAR_UUID, MOTOR_CHAR_UUID])

			# Find the BNO service and its characteristics.
			bno = device.find_serivce[BNO_SERVICE_UUID]
			yaw = bno.find_characteristic(YAW_CHAR_UUID)
			motor = bno.find_characteristic(MOTOR_CHAR_UUID)

			# subscribe to yaw value change notifications
			yaw.start_notify(received)
			print("staring main loop...")

			while True:
				# Flush serial inputs and outputs.
				## sip_puff_serial_port.flushInput()
				## sip_puff_serial_port.flushOutput()

				# Request data from sip/puff sensor.
				request_string = "r"
				## sip_puff_serial_port.write(request_string.encode() + b'x0a')

				# Pause between requesting and reading data.
				# time.sleep(0.025)

				# Read data from sip puff sensor.
				## new_selected_chord = sip_puff_serial_port.readline().rstrip().decode()

				new_selected_chord = 2

				if new_selected_chord != current_selected_chord:
					chord_to_display = str(new_selected_chord)
					## sip_puff_serial_port.write(chord_to_display.encode() + b'x0a')
					current_selected_chord = new_selected_chord

				last_pluck_time = pluck_time
				pluck_time = time.time()
				#if last_pluck_time is not None:
				#	print(f"Delay: {pluck_time - last_pluck_time}")
				#print(
				#	f" N Threads: {len(loom)}")
		finally:
			# Make sure device is disconnected on exit.
			device.disconnect()


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
