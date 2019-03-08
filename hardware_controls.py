import time

# GPIO imports
import RPi.GPIO as GPIO

class Encoder():
	
	def __init__(self, debounce_delay, track_a_pin_number, track_b_pin_number):	
		# initialise track numbers
		self.track_a_pin_number = track_a_pin_number
		self.track_b_pin_number = track_b_pin_number
		
		# set encoder track inputs and set intial value to be pulled up (on)
		GPIO.setup(self.track_a_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(self.track_b_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
		# initialise values
		self.track_a_value = GPIO.input(self.track_a_pin_number)
		self.track_b_value = GPIO.input(self.track_b_pin_number)
		
		# set the last known pin values based on the initialised values above
		self.last_track_a_value = self.track_a_value
		self.last_track_b_value = self.track_b_value
		self.clean_value = self.track_b_value
		
		self.last_debounce_time = time.time()
		self.debounce_delay = debounce_delay
		self.counter = 0
		self.print_flag = False
		
		
	def process(self):
		# read the value of track a
		incoming_track_a_value = GPIO.input(self.track_a_pin_number)
		
		# if the value of track a has changed since the last time this function was called...		
		if incoming_track_a_value != self.last_track_a_value:
			#...reset the last value of track a and...
			self.last_track_a_value = incoming_track_a_value
			#...read track b.
			incoming_track_b_value = GPIO.input(self.track_b_pin_number)
			
			# if the value of track b does not equal the clean value...
			if incoming_track_b_value != self.clean_value:
				#...set the clean value to that of track b.
				self.clean_value = incoming_track_b_value
				
				if (time.time() - self.last_debounce_time) > self.debounce_delay:
					self.last_debounce_time = time.time()
					return (incoming_track_a_value == incoming_track_b_value)

class Debounce():
	# class variables go here
	
	def __init__(self, debounce_delay, pin_number):
		
		# instance variables go here
		# set button pins to be inputs and set intial value to be pulled low (off)
		self.pin_number = pin_number
		GPIO.setup(self.pin_number, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
		self.debounce_delay = debounce_delay
		self.pin_state = GPIO.input(self.pin_number)
		self.last_pin_state = self.pin_state
		self.current_time = time.time()
		self.last_debounce_time = time.time()
		
	def process(self):
		# read the value from the GPIO pin
		incoming_pin_value = GPIO.input(self.pin_number)
		
		# if the pin value has changed...
		if incoming_pin_value != self.last_pin_state:
			# ...reset the debouncing timer
			self.last_debounce_time = time.time()
			 	 
		# has the debounce time been exceeded?...
		if (time.time() - self.last_debounce_time) > self.debounce_delay:
		# ...then this is the actual state of the button
			
			# if the button state has changed
			if incoming_pin_value != self.pin_state:
				self.pin_state = incoming_pin_value
	
				if self.pin_state == 1:
					self.last_pin_state = incoming_pin_value
					return 1
				elif self.pin_state == 0:
					self.last_pin_state = incoming_pin_value
					return 0
				
		self.last_pin_state = incoming_pin_value

	def get_last_pin_state(self):
		return self.last_pin_state
