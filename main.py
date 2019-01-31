# sip/puff variant
# -*- coding: utf-8 -*-
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
from Adafruit_BluefruitLE.services import UART

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

chord = 0
midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()

# constants
NUMBER_OF_CHORDS = 2
NUMBER_OF_STRINGS = 6


class ChordStrummer:
	global midiout
	c_major_chord_notes = [[0, 48, 52, 55, 60, 64],[0, 0, 50, 57, 62, 65],[40, 47, 52, 55, 59, 64],[0, 0, 53, 55, 60, 65],[43, 47, 50, 55, 59, 65],[0, 45, 52, 57, 60, 64],[0, 47, 50, 55, 62, 0]]

	def play_chord(self, chord_number, string_number):
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


def is_float(value):
	try:
		float(value)
		return True
	except ValueError:
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
	print('Disconnecting any connected UART devices...')
	UART.disconnect_devices()

	# Scan for BNO devices.
	print('Searching for BNO device...')
	try:
		adapter.start_scan()
		# Search for the first BNO device found (will time out after 60 seconds
		# but you can specify an optional timeout_sec parameter to change it).
		device = ble.find_device(name='motionwristband')

		if device is None:
			raise RuntimeError('Failed to find motionwristband device!')
	finally:
		# Make sure scanning is stopped before exiting.
		adapter.stop_scan()

	print('Connecting to device...')
	device.connect()
	# Will time out after 60 seconds, specify timeout_sec parameter
	# to change the timeout.

	# Connect to serial port
	sip_puff_serial_port = serial.Serial('/dev/tty.usbmodem1411111', 115200, timeout=0.1)
	# Pause to allow time for serial connection to be established.
	time.sleep(1)

	# open a MIDI port. Currently hard-wired to IAC driver.
	if available_ports:
		print(available_ports)
		midiout.open_port(1)

		# create class instances.
		myChord = ChordStrummer()

		# Intitialise variables.
		wristband_imu_value_as_float = 0.0
		new_wristband_position_as_segment_number = 0
		current_wristband_position_as_segment_number = 0

		# Flush serial inputs and outputs.
		sip_puff_serial_port.flushInput()
		sip_puff_serial_port.flushOutput()

		# Divide range of IMU into segments.
		wristband_segmenter = StringSegmenter(-61, 0, NUMBER_OF_STRINGS)

		# flush sip puff sensor
		sip_puff_serial_port.flushInput()
		sip_puff_serial_port.flushOutput()

		# Request data from sip puff sensor.
		request_string  = 'r'
		newline = '\n'
		sip_puff_serial_port.write(request_string.encode() + newline.encode())

		# Pause between requesting and reading data.
		time.sleep(0.025)

		#######################################
		# Read data from sip/puff switch.
		new_selected_chord = sip_puff_serial_port.readline().rstrip().decode()
		current_selected_chord = new_selected_chord
		chord_to_display = str(current_selected_chord)
		sip_puff_serial_port.write(chord_to_display.encode() + b'x0a')

		try:
			# Wait for service discovery to complete for at least the specified
			# service and characteristic UUID lists.  Will time out after 60 seconds
			# (specify timeout_sec parameter to override).
			print('Discovering services...')
			UART.discover(device)

			# Find the UART service and its characteristics.
			uart = UART(device)

			while True:
				# Flush serial inputs and outputs.
				sip_puff_serial_port.flushInput()
				sip_puff_serial_port.flushOutput()

				# Request data from sip/puff sensor.
				request_string  = "r"
				sip_puff_serial_port.write(request_string.encode() + b'x0a')

				# Pause between requesting and reading data.
				time.sleep(0.025)

				# Read data from sip puff sensor.
				new_selected_chord = sip_puff_serial_port.readline().rstrip().decode()

				# Read data from wristband
				# yaw_request_string = "y"
				uart.write(b'y\n')

				received = uart.read(timeout_sec=60)
				if received is not None:
				# Received data, print it out.
					print('Received: {0}'.format(received))
					if is_float(received):
						wristband_imu_value_as_float = float(received)
					print(wristband_imu_value_as_float)
				else:
					# Timeout waiting for data, None is returned.
					print('Received no data!')


				# Convert serial strings to float values.
				# if(is_float(wristbandImuValue)):
				# wristband_imu_value_as_float = float(wristbandImuValue)

				if new_selected_chord != current_selected_chord:
					chord_to_display = str(new_selected_chord)
					sip_puff_serial_port.write(chord_to_display.encode() + b'x0a')
					current_selected_chord = new_selected_chord

				# this will be the code for parsing the wristband.
				new_wristband_position_as_segment_number = wristband_segmenter.determine_segment(wristband_imu_value_as_float)

				if new_wristband_position_as_segment_number != current_wristband_position_as_segment_number:
					if wristband_segmenter.is_segment_a_string(new_wristband_position_as_segment_number):
						print("playing notes")

						# Request that the motor be switched on here.
						# motor.write_value(b'0x32\r')

						t1 = threading.Thread(target=myChord.play_chord, args=(int(current_selected_chord), wristband_segmenter.get_segment_as_string_number(new_wristband_position_as_segment_number)))
						t1.start()

					current_wristband_position_as_segment_number = new_wristband_position_as_segment_number
		finally:
			# Make sure device is disconnected on exit.
			device.disconnect()


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
