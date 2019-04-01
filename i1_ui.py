import time
# import all of the classes in 'controls'
from hardware_controls import *

# import all of the classes in 'menu'
from menu import *

# pressure sensor imports
import board
import busio
import adafruit_mprls

# GPIO imports
import RPi.GPIO as GPIO

# display imports
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

# inspect function attributes
from inspect import signature

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
print(width)
height = disp.height
print(height)
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# First define some constants to allow easy resizing of shapes.
PADDING = 2
BOTTOM = height-PADDING
MENU_ITEM_HEIGHT = 14
# Load font.
font = ImageFont.truetype('BodgeR.ttf', 12)

# create arrays of strings to dispaly as parameter values
root_note_values  = {0:'A', 1:'A#', 2:'B',
					 3:'C', 4:'C#', 5:'D',
					 6:'D#',7:'E',  8:'F',
					 9:'F#',10:'G',11:'G#'}
					 
chord_type_values = {0:'Major', 1:'Major 6', 2:'Major 7',
					 3:'minor', 4:'minor 6', 5:'minor 7',
					 6:'Dominant'}

# parameter name, current index, index, parameter value as string
parameter_container = dict()
# the container consists of the...
# name of the parameter
# the index point of the value which show be displayed
# an array of strings to display										   
parameter_container['effect_1_parameter_1'] = [0, {0:'0',
												   1:'1',
												   2:'2',
												   3:'3',}]
												   
parameter_container['effect_1_parameter_2'] = [0, {0:'0',
												   1:'1',
												   2:'2',
												   3:'3',}]

parameter_container['effect_1_parameter_3'] = [0, {0:'0',
												   1:'1',
												   2:'2',
												   3:'3',}]

parameter_container['effect_1_parameter_4'] = [0, {0:'0',
												   1:'1',
												   2:'2',
												   3:'3',}]	
												   
parameter_container['red_chord_root_note'] = [0, root_note_values]
parameter_container['green_chord_root_note'] = [0, root_note_values]
parameter_container['blue_chord_root_note'] = [0, root_note_values]
parameter_container['yellow_chord_root_note'] = [0, root_note_values]

parameter_container['red_chord_type'] = [0, chord_type_values]
parameter_container['green_chord_type'] = [0, chord_type_values]
parameter_container['blue_chord_type'] = [0, chord_type_values]
parameter_container['yellow_chord_type'] = [0, chord_type_values]

parameter_container['instrument'] = [0, {0:'Stratocaster',
											 1:'Telecaster',
											 2:'Les Paul',
										     3:'Acoustic'}]

parameter_container['effect_slot_1_type'] = [0, {0:'Off',
												 1:'Distortion',
												 2:'Flanger',
												 3:'Chorus'}]


parameter_container['effect_slot_2_type'] = [0, {0:'Off',
												 1:'Distortion',
												 2:'Flanger',
												 3:'Chorus'}]												 
												 										     

# create an instance of the menu controller
menu_controller = Menu_Controller()

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
root_note_text = ('Root Note', 'Value:')
chord_type_text = ('Chord Type', 'Value:', )

# dummy handler functions
def reconnect_bluetooth_handler():
	print('reconnecting to bluetooth')
	# it will take some time to conenct here - a try except block would be useful
	# delay to emulate connection time
	time.sleep(2)
	# if successful show success Splash_Page
	menu_controller.current_menu_location = '0000'
	# redraw the display
	menu_controller.redraw_display_flag = True
	# pause before returning to main menu
	time.sleep(1)
	# set menu location to be that of the main menu
	menu_controller.current_menu_location = ''
	# redraw the display
	menu_controller.redraw_display_flag = True
	
def instrument_selection_handler(parameter_name):
	
	index = parameter_container[parameter_name][0]
	selected_instrument = parameter_container[parameter_name][1][index]
	
	print('The selected instrument is {}'.format(selected_instrument))

def effect_selection_handler(parameter_name):
	print('The selected effect is {}'.format(selected_effect))
	
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

# create instances of each Menu_Page
main = List_Page(main_text, 'list', back_button_disabled=True)
_global = List_Page(global_text, 'list')
wristband = List_Page(wristband_text, 'list')
reconnect = Splash_Page(reconnect_text, 'splash')
connection_success = Splash_Page(connection_success_text, 'splash')
instrument = Selection_Page(instrument_text, 'selection', 'instrument', parameter_container, instrument_selection_handler)
effect = List_Page(effect_text, 'list')
effect_slot_1 = List_Page(effect_slot_text, 'list')
effect_slot_2 = List_Page(effect_slot_text, 'list')
effect_slot_1_type = Selection_Page(effect_type_text, 'selection', 'effect_slot_1_type', parameter_container, effect_selection_handler)
effect_slot_2_type = Selection_Page(effect_type_text, 'selection', 'effect_slot_2_type', parameter_container, effect_selection_handler)
effect_slot_1_parameter_1 = Value_Page(parameter_value_text, 'value', 'effect_1_parameter_1', parameter_container)
effect_slot_1_parameter_2 = Value_Page(parameter_value_text, 'value', 'effect_1_parameter_2', parameter_container)
effect_slot_2_parameter_1 = Value_Page(parameter_value_text, 'value', 'effect_1_parameter_3', parameter_container)
effect_slot_2_parameter_2 = Value_Page(parameter_value_text, 'value', 'effect_1_parameter_4', parameter_container)
chords = List_Page(chords_text, 'list')
red_chord_config = List_Page(chord_config_text, 'list')
green_chord_config = List_Page(chord_config_text, 'list')
blue_chord_config = List_Page(chord_config_text, 'list')
yellow_chord_config = List_Page(chord_config_text, 'list')
red_root_note = Value_Page(root_note_text, 'value', 'red_chord_root_note', parameter_container)
red_chord_type = Value_Page(chord_type_text, 'value', 'red_chord_type', parameter_container)
green_root_note = Value_Page(root_note_text, 'value', 'green_chord_root_note', parameter_container)
green_chord_type = Value_Page(chord_type_text, 'value', 'green_chord_type', parameter_container)
blue_root_note = Value_Page(root_note_text, 'value', 'blue_chord_root_note', parameter_container)
blue_chord_type = Value_Page(chord_type_text, 'value', 'blue_chord_type', parameter_container)
yellow_root_note = Value_Page(root_note_text, 'value', 'yellow_chord_root_note', parameter_container)
yellow_chord_type = Value_Page(chord_type_text, 'value', 'yellow_chord_type', parameter_container)

### Construct the Menu ###

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
menu_controller.structure['20'] = effect_slot_1 # Effect Slot 1
menu_controller.structure['21'] = effect_slot_2 # Effect Slot 2

# add a Menu_Page for each item listed in the chords Menu_Page
menu_controller.structure['30'] = red_chord_config # Red chord
menu_controller.structure['31'] = green_chord_config # Green chord
menu_controller.structure['32'] = blue_chord_config # Blue chord 
menu_controller.structure['33'] = yellow_chord_config # Yellow chord 

## Tier 3 ##
# add a Menu_Page for each item listed in the wristband Menu_Page
menu_controller.structure['000'] = reconnect 

# add a Menu_Page for each item listed in the effect_slot Menu_Page(s)
# Effect Slot 1
menu_controller.structure['200'] = effect_slot_1_type
menu_controller.structure['201'] = effect_slot_1_parameter_1 # Parameter 1
menu_controller.structure['202'] = effect_slot_1_parameter_2 # Parameter 2
# Effect Slot 2
menu_controller.structure['210'] = effect_slot_2_type
menu_controller.structure['211'] = effect_slot_2_parameter_1 # Parameter 1
menu_controller.structure['212'] = effect_slot_2_parameter_2 # Parameter 2

# add a Menu page for each item listed in the chord_config Menu_Page(s)
# Red chord
menu_controller.structure['300'] = red_root_note
menu_controller.structure['301'] = red_chord_type
# Green chord
menu_controller.structure['310'] = green_root_note
menu_controller.structure['311'] = green_chord_type
# Blue chord
menu_controller.structure['310'] = blue_root_note
menu_controller.structure['311'] = blue_chord_type
# Yellow chord
menu_controller.structure['320'] = yellow_root_note
menu_controller.structure['321'] = yellow_chord_type

## Tier 4 ##
# add a Menu page for each item listed in the reconnect Menu_Page
menu_controller.structure['0000'] = connection_success

# make each page aware of its location
for key, value in menu_controller.structure.items():
	value.location = key

# reconnect to bluetooth
wristband.assign_enter_function('Reconnect', reconnect_bluetooth_handler)

def draw_display(incoming_image):
	# clear the display
	disp.clear()
	# add the image
	disp.image(incoming_image)
	# refresh the display
	disp.display()
	
	# reset the display flag

	menu_controller.redraw_display_flag = False
	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
while True:
	# redraw the display if required.
	if menu_controller.redraw_display_flag == True:
		current_menu = menu_controller.get_current_page()
		draw_display(current_menu.get_image(menu_controller))
	
	# process the buttons
	if up_button.process() == 1:
		current_menu.on_up_button(menu_controller)
		
	if down_button.process() == 1:
		current_menu.on_down_button(menu_controller)
	
	if back_button.process() == 1:
		current_menu.on_back_button(menu_controller)
	
	if enter_button.process() == 1:
		# if the current menu is a Selection_Page pass in the parameter container
		if type(current_menu) is Selection_Page:
			current_menu.on_enter_event(menu_controller, parameter_container)
		else:
			current_menu.on_enter_event(menu_controller)
			
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
	menu_encoder_scan_result = menu_encoder.process()

	# check if any activity has taken place.
	if menu_encoder_scan_result != None:
		# the menu encoder only acts when a Value_Page is selected
		if type(current_menu) is Value_Page:
			# pass on the result of the scan to the menu page
			current_menu.on_encoder_event(menu_encoder_scan_result, menu_controller, parameter_container)
				
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
	
