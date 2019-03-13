import time
# import all of the classes in 'controls'
from hardware_controls import *

# pressure sensor imports
import board
import busio
import adafruit_mprls

# inspect function attributes
from inspect import signature

# GPIO imports
import RPi.GPIO as GPIO

# display imports
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# use GPIO numbering
GPIO.setmode(GPIO.BCM)

# Raspberry Pi pin configuration:
DISPLAY_RESET = 24

# button pin constants
UP_BUTTON_PIN = 5
DOWN_BUTTON_PIN = 6
BACK_BUTTON_PIN = 13
ENTER_BUTTON_PIN = 26
PRESET_ONE_BUTTON_PIN = 20
PRESET_TWO_BUTTON_PIN = 16
PRESET_THREE_BUTTON_PIN = 12
PRESET_FOUR_BUTTON_PIN = 7
SAVE_BUTTON_PIN = 8
POWER_BUTTON_PIN = 4
CHORD_CHANGE_BUTTON_PIN = 10

# encoder pin constants
MENU_ENCODER_CHANNEL_A_PIN = 9
MENU_ENCODER_CHANNEL_B_PIN = 11
VOLUME_ENCODER_CHANNEL_A_PIN = 14 
VOLUME_ENCODER_CHANNEL_B_PIN = 15

# encoder rotation constants
CLOCKWISE = 0
ANTI_CLOCKWISE = 1

# debounce time in seconds
DEBOUNCE_TIME = 0.05                                       

# pressure sensor intialisation
i2c = busio.I2C(board.SCL, board.SDA)
mpr = adafruit_mprls.MPRLS(i2c, psi_min=0, psi_max=25)

# hardware UI class instances
up_button = Debounce(DEBOUNCE_TIME, UP_BUTTON_PIN)
down_button = Debounce(DEBOUNCE_TIME, DOWN_BUTTON_PIN)
back_button = Debounce(DEBOUNCE_TIME, BACK_BUTTON_PIN)
enter_button = Debounce(DEBOUNCE_TIME, ENTER_BUTTON_PIN)
preset_one_button = Debounce(DEBOUNCE_TIME, PRESET_ONE_BUTTON_PIN)
preset_two_button = Debounce(DEBOUNCE_TIME, PRESET_TWO_BUTTON_PIN)
preset_three_button = Debounce(DEBOUNCE_TIME, PRESET_THREE_BUTTON_PIN)
preset_four_button = Debounce(DEBOUNCE_TIME, PRESET_FOUR_BUTTON_PIN)
save_button = Debounce(DEBOUNCE_TIME, SAVE_BUTTON_PIN)
power_button = Debounce(DEBOUNCE_TIME, POWER_BUTTON_PIN)
chord_change_button = Debounce(DEBOUNCE_TIME, CHORD_CHANGE_BUTTON_PIN)
menu_encoder = Encoder(DEBOUNCE_TIME, MENU_ENCODER_CHANNEL_A_PIN, MENU_ENCODER_CHANNEL_B_PIN)
volume_encoder = Encoder(DEBOUNCE_TIME, VOLUME_ENCODER_CHANNEL_A_PIN, VOLUME_ENCODER_CHANNEL_B_PIN)

# effect parameters
effect_1_parameter_1 = 0
effect_1_parameter_2 = 0
effect_2_parameter_1 = 0
effect_2_parameter_2 = 0

# display initialisation
# 128x64 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_64(rst=DISPLAY_RESET, i2c_address=0x3D)

disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# First define some constants to allow easy resizing of shapes.
PADDING = 2
BOTTOM = height-PADDING
MENU_ITEM_HEIGHT = 14
# Load font.
font = ImageFont.truetype('BodgeR.ttf', 12)

SELECTION_STRING = '> '
SPACE_STRING = '  '

class Menu_Controller:
	# keep track of the cursor position
	current_cursor_position = 0
	current_menu_location = ''
	structure = {None: None,}
	redraw_display_flag = True
		
	def increment_cursor_position(self):	
		# get the number of items in the currently selected menu but zero indexed
		menu_now = Menu_Controller.structure.get(Menu_Controller.current_menu_location)
		number_of_menu_items = len(menu_now.menu_items) - 1
		
		# wrap around if last menu item is reached.
		if Menu_Controller.current_cursor_position < number_of_menu_items:
			Menu_Controller.current_cursor_position += 1
		else:
			Menu_Controller.current_cursor_position = 0

	def decrement_cursor_position(self):
		# get the number of items in the currently selected menu but zero indexed
		menu_now = Menu_Controller.structure.get(Menu_Controller.current_menu_location)
		number_of_menu_items = len(menu_now.menu_items) - 1
		
		# wrap around if first menu item is reached.
		if Menu_Controller.current_cursor_position > 0:
			Menu_Controller.current_cursor_position -= 1
		else:
			Menu_Controller.current_cursor_position = number_of_menu_items
			
	def reset_cursor_position(self):
		# simply reset the position of the cursor to zero. 
		Menu_Controller.current_cursor_position = 0

	def move_menu_location_forwards(self):
		# append the current cursor position to show that we have progressed deeper into the menu at a certain point
		Menu_Controller.current_menu_location += str(Menu_Controller.current_cursor_position)

		# reset the cursor position
		self.reset_cursor_position()
		
	def move_menu_location_backwards(self):
		# remove the last item from the current_menu_location string
		# this shows that we have retreated by one menu level
		Menu_Controller.current_menu_location = Menu_Controller.current_menu_location[:-1]
		
		# reset the cursor position
		self.reset_cursor_position()
		
	def get_current_page(self):
		# return the currently selected menu
		return Menu_Controller.structure[Menu_Controller.current_menu_location]		

class Menu_Page:
	def __init__(self, text, menu_type, back_button_disabled=False):
		self.menu_items = text
		self.menu_functions = {None:None,}
		self.menu_type = menu_type
		self.back_button_disabled = back_button_disabled
		self.enter_button_disabled = False
		self.cursor_disabled = False
		self.encoder_clockwise_function = None
		self.encoder_anti_clockwise_function = None
		self.parameter_to_display = '31'
		
		# disable the cursor and enter button if Menu_Page type is 'Splash'
		if menu_type == 'splash':
			self.cursor_disabled = True
			self.enter_disabled = True
		
		# disable the cursor if Menu_Page type is 'Value'
		if menu_type == 'value':
			self.cursor_disabled = True
			
	def get_image(self, current_cursor_position):
		# create a new blank image
		local_image = Image.new('1', (width, height))

		# Get drawing object to draw on image.
		local_draw = ImageDraw.Draw(local_image)
	
		# a new list to add formatted menu string to.
		formatted_menu_strings = []
	
		# if the cursor is not disabled...
		if self.cursor_disabled != True:
			# ...create a new list to add formatted menu strings to and...
			formatted_menu_strings = []
			# ...format each string in the menu
			for index, menu_item in enumerate(self.menu_items):
				formatted_menu_strings.append(self.menu_string_generator(index, menu_item, current_cursor_position))

			# draw each item onto the image in the correct position
			for index, menu_string in enumerate(formatted_menu_strings):
				local_draw.text((PADDING,PADDING * (index + 1) + (MENU_ITEM_HEIGHT * index)), menu_string, font=font, fill=255)
		# else just	draw the unformatted strings to the display
		else:
			for index, menu_string in enumerate(self.menu_items):
				# check to see if a value needs to be displayed
				if menu_string == 'Value:':
					menu_string + ' ' + self.parameter_to_display
				local_draw.text((PADDING,PADDING * (index + 1) + (MENU_ITEM_HEIGHT * index)), menu_string, font=font, fill=255)
				
		return local_image
		
	def set_parameter_to_display(self, parameter):
		self.parameter_to_display = parameter
		
	# generate formatted strings which include selection marker and whitespace
	def menu_string_generator(self, menu_item_number, text_to_display, current_cursor_position):
		if menu_item_number == current_cursor_position:
			return SELECTION_STRING + text_to_display
		else:
			return SPACE_STRING + text_to_display
			
	def on_enter_button(self, menu_controller):
		# make sure that the Menu_Page is of type 'list'
		if self.menu_type == 'list':
			# get the text string at the current cursor position
			text_string = self.menu_items[menu_controller.current_cursor_position]
			
			# if a function has been assigned to the menu_item...
			if self.menu_functions.get(text_string) != None:
				#... get the function
				function_to_call = self.menu_functions.get(text_string)
				
				# get the siganture of the function
				function_signature = signature(function_to_call)
				# get the function parameters
				function_parameters = function_signature.parameters
				
				# count the number of parameters. if == 1 a location identifier is required
				if len(function_parameters) == 1:
					location_identifier = menu_controller.current_menu_location + str(menu_controller.current_cursor_position)
					function_to_call(location_identifier)
				else:
					function_to_call()
			else:
				# progress deeper into the menu
				menu_controller.move_menu_location_forwards()
				# indicate that the display needs to be redrawn
				menu_controller.redraw_display_flag = True
				
	def on_back_button(self, menu_controller):
		if self.back_button_disabled != True:
			menu_controller.move_menu_location_backwards()
			menu_controller.redraw_display_flag = True
			
	def on_down_button(self, menu_controller):
		if self.menu_type == 'list':
			menu_controller.increment_cursor_position()
			menu_controller.redraw_display_flag = True
			
	def on_up_button(self, menu_controller):
		if self.menu_type == 'list':
			menu_controller.decrement_cursor_position()
			menu_controller.redraw_display_flag = True
			
	def on_encoder_clockwise(self, menu_controller):
		self.encoder_clockwise_function(menu_controller.current_menu_location)
		menu_controller.redraw_display_flag = True
		
	def on_encoder_anti_clockwise(self, menu_controller):
		self.encoder_anti_clockwise_function(menu_controller.current_menu_location)
		menu_controller.redraw_display_flag = True
		
	def assign_enter_function(self, menu_item, function):
		# assign the incoming function to the menu item.
		self.menu_functions[menu_item] = function
		
	def assign_encoder_clockwise_function(self, function):
		self.encoder_clockwise_function = function
		
	def assign_encoder_anti_clockwise_function(self, function):
		self.encoder_anti_clockwise_function = function
		
# create text strings for each menu page
main_text = ('Global', 'Instrument', 'Effect', 'Chords')
global_text = ('Wristband',)
wristband_text = ('Reconnect',)
reconnect_text = ('Searching', 'please wait...')
connection_success_text = ('Connection successful!', 'Returning to main menu...')
instrument_text = ('Stratocaster', 'Telecaster', 'Les Paul', 'Acoustic')
effect_text = ('Slot 1', 'Slot 2')
effect_slot_text = ('Type', 'Parameter 1', 'Parameter 2')
effect_type_text = ('Off', 'Distortion', 'Flanger', 'Chorus')
parameter_value_text = ('Parameter Name', 'Value:')
chords_text = ('Red', 'Green', 'Blue', 'Yellow')
chord_config_text = ('Root Note', 'Type')
root_note_text = ('Root Note:', 'A')
chord_type_text = ('Chord Type:', 'Major', )

# create instances of each Menu_Page
main = Menu_Page(main_text, 'list', back_button_disabled=True)
_global = Menu_Page(global_text, 'list')
wristband = Menu_Page(wristband_text, 'list')
reconnect = Menu_Page(reconnect_text, 'splash')
connection_success = Menu_Page(reconnect_text, 'splash')
instrument = Menu_Page(instrument_text, 'list')
effect = Menu_Page(effect_text, 'list')
effect_slot = Menu_Page(effect_slot_text, 'list')
effect_type = Menu_Page(effect_type_text, 'list')
effect_parameter = Menu_Page(parameter_value_text, 'value')
chords = Menu_Page(chords_text, 'list')
chord_config = Menu_Page(chord_config_text, 'list')
root_note = Menu_Page(root_note_text, 'value')
chord_type = Menu_Page(chord_type_text, 'value')

# assign functions to Menu_Items

# dummy handler functions
def reconnect_bluetooth_handler():
	print('reconnecting to bluetooth')
	
def instrument_selection_handler(location_identifier):
	if location_identifier == '10':
		print('Loading Stratocaster')
	elif location_identifier == '11':
		print('Loading Telecaster')
	elif location_identifier == '12':
		print('Loading Les Paul')
	elif location_identifier == '13':
		print('Loading Acoustic')
	
def effect_selection_handler(location_identifier):
	if location_identifier == '2000':
		print('Switching off the effect in Slot 1')
	if location_identifier == '2001':
		print('Loading Distorion in Slot 1')
	if location_identifier == '2002':
		print('Loading Flanger in Slot 1')
	if location_identifier == '2003':
		print('Loading Chorus in Slot 1')
	if location_identifier == '2100':
		print('Switching off the effect in Slot 2')
	if location_identifier == '2101':
		print('Loading Distorion in Slot 2')
	if location_identifier == '2102':
		print('Loading Flanger in Slot 2')
	if location_identifier == '2103':
		print('Loading Chorus in Slot 2')
		
def root_note_selection_handler(location_identifier):
	if location_identifier == '10':
		print('Loading Stratocaster')
	elif location_identifier == '11':
		print('Loading Telecaster')
	elif location_identifier == '12':
		print('Loading Les Paul')
	elif location_identifier == '13':
		print('Loading Acoustic')

# reconnect to bluetooth
wristband.assign_enter_function('Reconnect', reconnect_bluetooth_handler)
# load an instrument 
instrument.assign_enter_function('Stratocaster', instrument_selection_handler)
instrument.assign_enter_function('Telecaster', instrument_selection_handler)
instrument.assign_enter_function('Les Paul', instrument_selection_handler)
instrument.assign_enter_function('Acoustic', instrument_selection_handler)
# switch off effect
effect_type.assign_enter_function('Off', effect_selection_handler)
effect_type.assign_enter_function('Distortion', effect_selection_handler)
effect_type.assign_enter_function('Flanger', effect_selection_handler)
effect_type.assign_enter_function('Chorus', effect_selection_handler)

# dummy encoder functions 
def increment_parameter_value(location_identifier):
	global effect_1_parameter_1
	global effect_1_parameter_2
	global effect_2_parameter_1
	global effect_2_parameter_2
	
	# Effect 1, Parameter 1 value
	if location_identifier == '201':
		if effect_1_parameter_1 < 127:
			effect_1_parameter_1 += 1
	
	# Effect 1, Parameter 2 value		
	if location_identifier == '202':
		if effect_1_parameter_2 < 127:
			effect_1_parameter_2 += 1
				
	# Effect 2, Parameter 1 value
	if location_identifier == '211':
		if effect_2_parameter_1 < 127:
			effect_2_parameter_1 += 1
			
	# Effect 2, Parameter 2 value		
	if location_identifier == '212':
		if effect_2_parameter_2 < 127:
			effect_2_parameter_2 += 1

def decrement_parameter_value(location_identifier):
	global effect_1_parameter_1
	global effect_1_parameter_2
	global effect_2_parameter_1
	global effect_2_parameter_2
	
	# Effect 1, Parameter 1 value
	if location_identifier == '201':
		if effect_1_parameter_1 > 0:
			effect_1_parameter_1 -= 1
	
	# Effect 1, Parameter 2 value
	if location_identifier == '202':
		if effect_1_parameter_2 > 0:
			effect_1_parameter_2 -= 1
	
	# Effect 2, Parameter 1 value
	if location_identifier == '211':
		if effect_2_parameter_1 > 0:
			effect_2_parameter_1 -= 1
	
	# Effect 2, Parameter 2 value
	if location_identifier == '212':
		if effect_2_parameter_2 > 0:
			effect_2_parameter_2 -= 1

effect_parameter.assign_encoder_clockwise_function(increment_parameter_value)
effect_parameter.assign_encoder_anti_clockwise_function(decrement_parameter_value)


### Construct the Menu ###
menu_controller = Menu_Controller()

# dictionary keys are used to determine location
# the number of characters in the dicationary key indicates the tier of the menu
# menu items listed on each page are numbered using zero-indexing

## Tier 0 ##
# add the top Menu_Page to the menu dictionary
menu_controller.structure[''] = main

## Tier 1 ##
# add Menu_Page for each item listed in the top Menu_Page 
menu_controller.structure['0'] = _global
menu_controller.structure['1'] = instrument
menu_controller.structure['2'] = effect
menu_controller.structure['3'] = chords

## Tier 2 ##
# add a Menu_Page for each item listed in the _global Menu_Page
menu_controller.structure['00'] = wristband

# add a Menu_Page for each item listed in the effect Menu_Page
menu_controller.structure['20'] = effect_slot # Effect Slot 1
menu_controller.structure['21'] = effect_slot # Effect Slot 2

# add a Menu_Page for each item listed in the chords Menu_Page
menu_controller.structure['30'] = chord_config # Red chord
menu_controller.structure['31'] = chord_config # Green chord
menu_controller.structure['32'] = chord_config # Blue chord 
menu_controller.structure['33'] = chord_config # Yellow chord 

## Tier 3 ##
# add a Menu_Page for each item listed in the wristband Menu_Page
menu_controller.structure['000'] = reconnect 

# add a Menu_Page for each item listed in the effect_slot Menu_Page(s)
# Effect Slot 1
menu_controller.structure['200'] = effect_type
menu_controller.structure['201'] = effect_parameter # Parameter 1
menu_controller.structure['202'] = effect_parameter # Parameter 2
# Effect Slot 2
menu_controller.structure['210'] = effect_type
menu_controller.structure['211'] = effect_parameter # Parameter 1
menu_controller.structure['212'] = effect_parameter # Parameter 2

# add a Menu page for each item listed in the chord_config Menu_Page(s)
# Red chord
menu_controller.structure['300'] = root_note
menu_controller.structure['301'] = chord_type
# Green chord
menu_controller.structure['310'] = root_note
menu_controller.structure['311'] = chord_type
# Blue chord
menu_controller.structure['310'] = root_note
menu_controller.structure['311'] = chord_type
# Yellow chord
menu_controller.structure['320'] = root_note
menu_controller.structure['321'] = chord_type

## Tier 4 ##
# add a Menu page for each item listed in the reconnect Menu_Page
menu_controller.structure['0000'] = connection_success

# set redraw_display_flag to True so display is drawn on first iteration of main loop
redraw_display_flag = True

def draw_display(incoming_image):
	# clear the display
	disp.clear()
	# add the image
	disp.image(incoming_image)
	# refresh the display
	disp.display()
	
	# reset the display flag
	global redraw_display_flag 
	menu_controller.redraw_display_flag = False
	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
while True:

	# redraw the display if required.
	if menu_controller.redraw_display_flag == True:
		current_menu = menu_controller.get_current_page()
		draw_display(current_menu.get_image(menu_controller.current_cursor_position))
		print(effect_1_parameter_1)
	
	# process the buttons
	if up_button.process() == 1:
		current_menu.on_up_button(menu_controller)
		
	if down_button.process() == 1:
		current_menu.on_down_button(menu_controller)
	
	if back_button.process() == 1:
		current_menu.on_back_button(menu_controller)
	
	if enter_button.process() == 1:
		current_menu.on_enter_button(menu_controller)
			
	if preset_one_button.process() == 1:
		print("Preset-one button pressed")
		
	if preset_two_button.process() == 1:
		print("Preset-two button pressed")
		
	if preset_three_button.process() == 1:
		print("Preset-three button pressed")
		
	if preset_four_button.process() == 1:
		print("Preset-four button pressed")
		
	if save_button.process() == 1:
		print("Save button pressed")
		
	if power_button.process() == 1:
		print("Power button pressed")
	
	if chord_change_button.process() == 1:
		print("Chord Change button pressed")
	
	# process the menu encoder
	menu_encoder_scan = menu_encoder.process()

	# check if any activity has taken place. if it has...
	if menu_encoder_scan != None:
		#... check to see if a 'value' Menu_Page is selected.
		if current_menu.menu_type == 'value':
			# call the appropriate function 
			if menu_encoder_scan == CLOCKWISE:
				current_menu.on_encoder_clockwise(menu_controller)
			elif menu_encoder_scan == 1:
				current_menu.on_encoder_anti_clockwise(menu_controller)
				
	# process the volume encoder
	volume_encoder_scan = volume_encoder.process()
	
	# check if any activity has taken place. if it has...
	if volume_encoder_scan != None:
		#... check the direction the encoder has been rotated
		if volume_encoder_scan == 0:
			print('volume encoder turned clockwise')
		elif volume_encoder_scan == 1:
			print('volume encoder turned anti-clockwise')
			
	#print(mpr.pressure)
	
