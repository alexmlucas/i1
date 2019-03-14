from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

# inspect function attributes
from inspect import signature

SELECTION_STRING = '> '
SPACE_STRING = '  '
WIDTH = 128
HEIGHT = 64

# First define some constants to allow easy resizing of shapes.
PADDING = 2
BOTTOM = HEIGHT-PADDING
MENU_ITEM_HEIGHT = 14
# Load font.
font = ImageFont.truetype('BodgeR.ttf', 12)

CLOCKWISE = 0
ANTI_CLOCKWISE = 1

class Menu_Controller:
	# keep track of the cursor position
	cursor_position = 0
	current_menu_location = ''
	structure = dict()
	redraw_display_flag = True
		
	def increment_cursor_position(self):	
		# get the number of items in the currently selected menu but zero indexed
		menu_now = Menu_Controller.structure.get(Menu_Controller.current_menu_location)
		number_of_menu_items = len(menu_now.menu_items) - 1
		
		# wrap around if last menu item is reached.
		if Menu_Controller.cursor_position < number_of_menu_items:
			Menu_Controller.cursor_position += 1
		else:
			Menu_Controller.cursor_position = 0

	def decrement_cursor_position(self):
		# get the number of items in the currently selected menu but zero indexed
		menu_now = Menu_Controller.structure.get(Menu_Controller.current_menu_location)
		number_of_menu_items = len(menu_now.menu_items) - 1
		
		# wrap around if first menu item is reached.
		if Menu_Controller.cursor_position > 0:
			Menu_Controller.cursor_position -= 1
		else:
			Menu_Controller.cursor_position = number_of_menu_items
			
	def reset_cursor_position(self):
		# simply reset the position of the cursor to zero. 
		Menu_Controller.cursor_position = 0

	def move_menu_location_forwards(self):
		# append the current cursor position to show that we have progressed deeper into the menu at a certain point
		Menu_Controller.current_menu_location += str(Menu_Controller.cursor_position)

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
		
class Menu_Page(object):
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
		self.location = None
		
		# disable the cursor and enter button if Menu_Page type is 'Splash'
		if menu_type == 'splash':
			self.cursor_disabled = True
			self.enter_disabled = True
		
		# disable the cursor if Menu_Page type is 'Value'
		if menu_type == 'value':
			self.cursor_disabled = True
			
	def get_image(self, cursor_position):
		# create a new blank image
		local_image = Image.new('1', (WIDTH, HEIGHT))

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
				formatted_menu_strings.append(self.menu_string_generator(index, menu_item, cursor_position))

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
			
	def on_enter_event(self, menu_controller):
		# make sure that the Menu_Page is of type 'list'
		if self.menu_type == 'list':
			# get the text string at the current cursor position
			text_string = self.menu_items[menu_controller.cursor_position]
			
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
		
	def assign_enter_function(self, menu_item, function):
		# assign the incoming function to the menu item.
		self.menu_functions[menu_item] = function

		
class List_Page(Menu_Page):
	
	def get_image(self, menu_controller):
		# get the cursor positon
		cursor_position = menu_controller.cursor_position
		
		# create a new blank image
		local_image = Image.new('1', (WIDTH, HEIGHT))
		
		# Get drawing object to draw on image.
		local_draw = ImageDraw.Draw(local_image)

		# ...create a new list to add formatted menu strings to and...
		formatted_menu_strings = []
		
		# ...format each string in the menu
		for index, menu_item in enumerate(self.menu_items):
			formatted_menu_strings.append(self.menu_string_generator(index, menu_item, cursor_position))

			# draw each item onto the image in the correct position
			for index, menu_string in enumerate(formatted_menu_strings):
				local_draw.text((PADDING,PADDING * (index + 1) + (MENU_ITEM_HEIGHT * index)), menu_string, font=font, fill=255)		
		
		return local_image
		
	def on_enter_event(self, menu_controller):

			# get the text string at the current cursor position
			text_string = self.menu_items[menu_controller.cursor_position]
			
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
					location_identifier = menu_controller.current_menu_location + str(menu_controller.cursor_position)
					function_to_call(location_identifier)
				else:
					function_to_call()
			else:
				# progress deeper into the menu
				menu_controller.move_menu_location_forwards()
				# indicate that the display needs to be redrawn
				menu_controller.redraw_display_flag = True
				
	# generate formatted strings which include selection marker and whitespace
	def menu_string_generator(self, menu_item_number, text_to_display, cursor_position):
		if menu_item_number == cursor_position:
			return SELECTION_STRING + text_to_display
		else:
			return SPACE_STRING + text_to_display
	
		
class Value_Page(Menu_Page):
	
	def __init__(self, text, menu_type, parameter_name):
		Menu_Page.__init__(self, text, menu_type)
		self.parameter_name = parameter_name
		self.value_to_draw = '0'
		self.max_value = 127
	
	def get_image(self, menu_controller):
		# create a new blank image
		local_image = Image.new('1', (WIDTH, HEIGHT))
		
		# Get drawing object to draw on image.
		local_draw = ImageDraw.Draw(local_image)
		
		for index, menu_string in enumerate(self.menu_items):
			# check to see if a value needs to be displayed
			if menu_string == 'Value:':
				menu_string += ' ' 
				menu_string += self.value_to_draw
			local_draw.text((PADDING,PADDING * (index + 1) + (MENU_ITEM_HEIGHT * index)), menu_string, font=font, fill=255)
		
		return local_image
		
	def on_encoder_event(self, event, menu_controller, parameter_container):
		
		# get the maximum value of the parameter (zero indexed)
		max_parameter_value = len(parameter_container[self.parameter_name][1]) - 1
		
		# check the direction of the encoder event and act accordingly
		if event == CLOCKWISE:
			# if the parameter value is less than the maximum...
			if parameter_container[self.parameter_name][0] < max_parameter_value:
				# increment.
				parameter_container[self.parameter_name][0] += 1
		elif event == ANTI_CLOCKWISE:
			# if the parameter value is greater than the minimum...
			if parameter_container[self.parameter_name][0] > 0:
				#... decrement
				parameter_container[self.parameter_name][0] -= 1
		
		# get the string that needs to be drawn on the menu image
		index = parameter_container[self.parameter_name][0]
		self.value_to_draw = parameter_container[self.parameter_name][1][index]
		
		# indicate that the display needs to be redrawn			
		menu_controller.redraw_display_flag = True
	
	


	
		
