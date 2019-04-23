import time

# pressure sensor imports
import board
import busio
import adafruit_mprls

NUMBER_OF_PRESSURE_READINGS = 8
PRESSURE_THRESHOLD = 1000
SIP_DETECTED = 1
SIP_NOT_DETECTED = 0
# the number of chords is zero indexed
NUMBER_OF_CHORDS = 3

class Sip_Sensor:
	def __int__(self):
		# pressure sensor intialisation
		self.i2c = busio.I2C(board.SCL, board.SDA)
		self.mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)
		self.currently_selected_chord = 0
		self.pressure_sensor_current_state = SIP_NOT_DETECTED
		self.pressure_sensor_previous_state = SIP_NOT_DETECTED
		self.pressure_total = 0
		self.pressure_average = 0
		self.pressure_read_index = 0
		self.pressure_readings = []
		self.counter = 0
		
		# initialise array of pressure readings
		while self.counter < NUMBER_OF_PRESSURE_READINGS:
			self.pressure_readings.append(0)
			self.counter += 1
			
	def increment_chord_selection(self):
		if self.currently_selected_chord < NUMBER_OF_CHORDS:
			self.currently_selected_chord += 1
		else:
			# wrap around to first chord if not less that NUMBER_OF_CHORDS
			self.currently_selected_chord = 0
	  
	# simplify pressure reading to binary states
	def determine_pressure_state(self, incoming_pressure_average):
		if incoming_pressure_average < PRESSURE_THRESHOLD:
			return SIP_DETECTED
		else:
			return SIP_NOT_DETECTED
			
	def process(self):
		# subtract the last reading
		self.pressure_total = self.pressure_total - self.pressure_readings[self.pressure_read_index]
		
		# read from the sensor
		self.pressure_readings[self.pressure_read_index] = self.mpr.pressure
		
		# add the reading to the total
		self.pressure_total = self.pressure_total + self.pressure_readings[self.pressure_read_index]
		
		# advance to the next position in the array
		self.pressure_read_index += 1
		
		# if we're at the end of the array...
		if self.pressure_read_index >= NUMBER_OF_PRESSURE_READINGS:
			# ...wrap around to the beginning.
			self.pressure_read_index = 0
			
		# calculate the average
		self.pressure_average = self.pressure_total / NUMBER_OF_PRESSURE_READINGS
		
		self.pessure_sensor_current_state = self.determine_pressure_state(self.pressure_average)
		
		if self.pressure_sensor_current_state == SIP_DETECTED and self.pressure_sensor_previous_state == SIP_NOT_DETECTED:
			increment_chord_selection()
			# update the previous state of the pressure sensor ready for the next interation
			self.pressure_sensor_previous_state = SIP_DETECTED
			print('value incremented')
		
		if self.pressure_sensor_current_state == SIP_NOT_DETECTED and self.pressure_sensor_previous_state == SIP_DETECTED:
			# update the previous state of the pressure sensor ready for the next interation
			self.pressure_sensor_previous_state = SIP_NOT_DETECTED
			
	def get_currently_selected_chord(self):
		return self.currently_selected_chord
	
