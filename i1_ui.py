import time
# import all of the classes in 'controls'
from hardware_controls import *

# pressure sensor imports
import board
import busio
import adafruit_mprls

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

menu_top = ('Global', 'Instrument', 'Effect', 'Chords')
menu_global = ('Wristband',)
menu_wristband = ('Reconnect',)
menu_reconnect = ('Searching', 'please wait...')
menu_connection_successful = ('Connection successful!', 'Returning to main menu...')
menu_instrument = ('Stratocaster', 'Telecaster', 'Les Paul', 'Acoustic')
menu_effect = ('Slot 1', 'Slot 2')
menu_effect_slot = ('Type', 'Parameter 1', 'Parameter 2')
menu_effect_type = ('Off', 'Disortion', 'Flanger', 'Chorus')
menu_parameter_value = ('Parameter Name', 'Value 0-127')
menu_chord = ('Red', 'Green', 'Blue', 'Yellow')
menu_chord_configuration = ('Root Note', 'Type')

# assign a location value to each menu
menu = {'0':menu_top, '00':menu_global, '000': menu_wristband, '0000': menu_reconnect}
# keep track of the menu's where the cursor is disabled
menus_with_cursor_disabled = (menu_reconnect)
# keep track of the end points of each menu
menu_ends = (menu_reconnect)

# keep track of the cursor position and menu location
current_cursor_position = 0
current_menu_location = '0'

# a flag to disable back button when at top tier of the menu.
at_menu_start = True
# a flag to disable enter button when at the bottom tier of the menu.
at_menu_end = True

# generate formatted strings which include selection marker and whitespace
def menu_string_generator(menu_item_number, text_to_display):
	if menu_item_number == current_cursor_position:
		return SELECTION_STRING + text_to_display
	else:
		return SPACE_STRING + text_to_display

# set redraw_display_flag to True so display is drawn on first iteration of main loop
redraw_display_flag = True

def draw_display(incoming_menu):
	# create a new blank image
	local_image = Image.new('1', (width, height))

	# Get drawing object to draw on image.
	local_draw = ImageDraw.Draw(local_image)
	
	# a new list to add formatted menu string to.
	formatted_menu_strings = []
	
	# format each string in the menu
	for index, menu_item in enumerate(incoming_menu):
		formatted_menu_strings.append(menu_string_generator(index, menu_item)) 

	# draw each item onto the image in the correct position
	for index, menu_string in enumerate(formatted_menu_strings):
		local_draw.text((PADDING,PADDING * (index + 1) + (MENU_ITEM_HEIGHT * index)), menu_string, font=font, fill=255)
	
	# clear the display
	disp.clear()
	# add the image
	disp.image(local_image)
	# refresh the display
	disp.display()
	
	# reset the display flag
	global redraw_display_flag 
	redraw_display_flag = False
	
def increment_cursor_position():
	# create a global reference to allow a new value to be assigned to currently_selection_menu_item
	global current_cursor_position
	
	# get the number of items in the currently selected menu but zero indexed
	number_of_menu_items = len(menu.get(current_menu_location)) - 1
	
	# wrap around if last menu item is reached.
	if current_cursor_position < number_of_menu_items:
		current_cursor_position += 1
	else:
		current_cursor_position = 0

def decrement_cursor_position():
	# create a global reference to allow a new value to be assigned to currently_selection_menu_item
	global current_cursor_position
	
	# get the number of items in the currently selected menu but zero indexed
	number_of_menu_items = len(menu.get(current_menu_location)) - 1
	
	# wrap around if first menu item is reached.
	if current_cursor_position > number_of_menu_items:
		current_cursor_position -= 1
	else:
		current_cursor_position = number_of_menu_items
		
def reset_cursor_position():
	# simply reset the position of the cursor to zero.
	global current_cursor_position 
	current_cursor_position = 0

def move_menu_location_forwards():
	global current_menu_location
	
	# enable back button if we're moving past the first tier of the menu
	if current_menu_location == '0':
		global at_menu_start
		at_menu_start = False
	
	# append the current cursor position to show that we have progressed deeper into the menu at a certain point
	current_menu_location += str(current_cursor_position)

	# reset the cursor position
	reset_cursor_position()
	
	# disable the enter button if we're at the end of the menu
	for end in menu_ends:
		if end == menu.get(current_menu_location):
			at_menu_end = True
	
	print(current_menu_location)
	
def move_menu_location_backwards():
	# remove the last item from the current_menu_location string
	# this shows that we have retreated by one menu level
	global current_menu_location
	current_menu_location = current_menu_location[:-1]
	
	# reset the cursor position
	reset_cursor_position()
	
	# disable back button if at top tier of the menu
	if current_menu_location == '0':
		global at_menu_start
		at_menu_start = True
	
	print(current_menu_location)
	                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
while True:
	# redraw the display if required.
	if redraw_display_flag == True:
		draw_display(menu.get(current_menu_location))
	
	# process the buttons
	if up_button.process() == 1:
		decrement_cursor_position()
		# redraw the display on next iteration
		redraw_display_flag = True
		print("Up button pressed")
		
	if down_button.process() == 1:
		increment_cursor_position()
		# redraw the display on next iteration
		redraw_display_flag = True	
		print("Down button pressed")
	
	if back_button.process() == 1:
		# only on back button event if we're not at the top tier of the menu.
		if at_menu_start != True:
			move_menu_location_backwards()
			# redraw the display on next iteration
			redraw_display_flag = True
			print("Back button pressed")
	
	if enter_button.process() == 1:
		if at_menu_end != True:
			move_menu_location_forwards()
			redraw_display_flag = True
			print("Enter button pressed")
			
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

	if menu_encoder_scan != None:
		if menu_encoder_scan == False:
			print('menu encoder turned clockwise')
		elif menu_encoder_scan == True:
			print('menu encoder turned anti-clockwise')
	
	# process the volume encoder
	volume_encoder_scan = volume_encoder.process()

	if volume_encoder_scan != None:
		if volume_encoder_scan == False:
			print('volume encoder turned clockwise')
		elif volume_encoder_scan == True:
			print('volume encoder turned anti-clockwise')
			
	#print(mpr.pressure)
	
