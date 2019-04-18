// Display includes
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Button includes
#include "Simple_Button.h"
#include "Shift_Register_Button.h"
#include "Simple_Encoder.h"

// Menu includes
#include "Menu_Page.h"
#include "Menu_Controller.h"
#include "Parameter_Container.h"

#define OLED_RESET 15

// Create an instance of the display
Adafruit_SSD1306 display(OLED_RESET);

// Define the debounce time in milliseconds
#define DEBOUNCE_TIME 50

// Define the encoder pins
#define ENCODER_PIN_A 5
#define ENCODER_PIN_B 6

// Define the button/switch pins
#define RECONNECT_BTN_PIN 20
#define POWER_BTN_PIN 14
#define ACCESS_SWT_PIN 11

// Define button bits
#define PLAY_BTN_BIT 0
#define STOP_BTN_BIT 1
#define SONG_1_BTN_BIT 2
#define SONG_2_BTN_BIT 3
#define SONG_3_BTN_BIT 4
#define SONG_4_BTN_BIT 5
#define BACK_BTN_BIT 6
#define ENTER_BTN_BIT 7

// Define the shift register pins.
#define SHIFT_REG_LATCH 8
#define SHIFT_REG_DATA 9
#define SHIFT_REG_CLOCK 7

// Define the min & max cursor values
#define MIN_CURSOR_VALUE 0
#define MAX_CURSOR_VALUE 2

// Define characters to be sent as serial strings.
const char RECONNECT_CHAR PROGMEM = 'a'; 
const char POWER_CHAR PROGMEM = 'b';
const char ACCESS_SWT_CHAR PROGMEM = 'c';
const char PLAY_CHAR PROGMEM = 'd';
const char STOP_CHAR PROGMEM = 'e';
const char SONG_1_CHAR PROGMEM = 'f';
const char SONG_2_CHAR PROGMEM = 'g';
const char SONG_3_CHAR PROGMEM = 'h';
const char SONG_4_CHAR PROGMEM = 'i';
const char BACK_CHAR PROGMEM = 'j';
const char ENTER_CHAR PROGMEM = 'k';

const char song[] PROGMEM = "Song";
const char guitar[] PROGMEM = "Guitar";
const char zone[] PROGMEM = "Zone";
const char mix_levels[] PROGMEM = "Mix Levels";
const char classic_rock[] PROGMEM = "Classic Rock";
const char hard_rock[] PROGMEM = "Hard Rock";
const char acoustic[] PROGMEM = "Acoustic";
const char red_zone[] PROGMEM = "Red Zone";
const char green_zone[] PROGMEM = "Green Zone";
const char blue_zone[] PROGMEM = "Blue Zone";
const char scale[] PROGMEM = "Scale";
const char root[] PROGMEM = "Root";
const char scale_param[] PROGMEM = "Major, Minor, Blues, Pent. Major. Pent. Minor, Major Chord, Minor Chord";
const char root_param[] PROGMEM = "A, A#, B, C, C#, D, D#, E, F, F#, G, G#";
const char guitar_level[] PROGMEM = "Guitar Level";
const char backing_level[] PROGMEM = "Backing Level";
const char master_level[] PROGMEM = "Master Level";
const char test_array[] PROGMEM = "test";
const char flash_test PROGMEM = 'f';

// Menu locations
const char main_menu_location PROGMEM = '0';

// Pointers to menu locations
const char *p_main_menu_location = &main_menu_location;

// An array of constant pointers to constant chars?
const char *const main_menu_txt[] PROGMEM = {song, guitar, zone, mix_levels};
const char *const guitar_menu_txt[] PROGMEM = {guitar, classic_rock, hard_rock, acoustic};

// Define a variable to hold the data from the shift register
byte shift_reg_byte = 0;

// Create Simple_Button instances
Simple_Button reconnect_button(RECONNECT_BTN_PIN, DEBOUNCE_TIME, RECONNECT_CHAR);
Simple_Button power_button(POWER_BTN_PIN, DEBOUNCE_TIME, POWER_CHAR);
Simple_Button access_switch(ACCESS_SWT_PIN, DEBOUNCE_TIME, ACCESS_SWT_CHAR);

// Create Shift_Register_Button instances
Shift_Register_Button play_button(PLAY_BTN_BIT, DEBOUNCE_TIME, PLAY_CHAR);
Shift_Register_Button stop_button(STOP_BTN_BIT, DEBOUNCE_TIME, STOP_CHAR);
Shift_Register_Button song_1_button(SONG_1_BTN_BIT, DEBOUNCE_TIME, SONG_1_CHAR);
Shift_Register_Button song_2_button(SONG_2_BTN_BIT, DEBOUNCE_TIME, SONG_2_CHAR);
Shift_Register_Button song_3_button(SONG_3_BTN_BIT, DEBOUNCE_TIME, SONG_3_CHAR);
Shift_Register_Button song_4_button(SONG_4_BTN_BIT, DEBOUNCE_TIME, SONG_4_CHAR);
Shift_Register_Button back_button(BACK_BTN_BIT, DEBOUNCE_TIME, BACK_CHAR);
Shift_Register_Button enter_button(ENTER_BTN_BIT, DEBOUNCE_TIME, ENTER_CHAR);

// Create Simple_Encoder instance.
Simple_Encoder selection_encoder;

// A pointer to an array of constant pointers to constant chars.
const char *const *menu_text_pointer;

// Byte for storing incoming serial data.
int incomingByte = 0;

// String representing the current menu location.
char current_menu_location[] = {""};

// Buffer for reading menu text.
char string_buffer[30];

// Read and monitior encoder position.
int current_encoder_position, last_encoder_position;

// Create an instance of Menu_Controller.
Menu_Controller menu_controller(MIN_CURSOR_VALUE, MAX_CURSOR_VALUE);

// Create a pointer to the menu_controller
Menu_Controller *p_menu_controller = &menu_controller;

// Instance of parameter container
Parameter_Container parameter_container;

// Pointer to parameter container
Parameter_Container *p_parameter_container = &parameter_container;

// Create Menu_Page instances.
Menu_Page main_menu("list", p_main_menu_location, p_menu_controller, p_parameter_container);
//Menu_Page guitar_menu("selection");
//Menu_Page zone_menu("list");
//Menu_Page mix_levels_menu("list");

// Pointer to current Menu_Page
Menu_Page *p_current_menu_page = &main_menu;


/*// Structure for parameter values.
struct parameter_container{
  int currently_selected_song = 0;
} parameters;

// Pointer to parameter container
parameter_container *p_parameters;
*/

void setup() {
  menu_text_pointer = main_menu_txt;
  main_menu.set_text(menu_text_pointer);

  menu_text_pointer = guitar_menu_txt;
  //guitar_menu.set_text(menu_text_pointer);

  Serial.begin(9600);
  
  // Initialise the display with the 12C address 0x3D
  display.begin(SSD1306_SWITCHCAPVCC, 0x3D);
  display.setTextSize(1);
  display.setTextColor(WHITE);
  
  // Clear the display.
  display.clearDisplay();
  display.setCursor(0,0);
  display.println(F("Hello Alex!"));
  display.display();
 
  selection_encoder.initialise(ENCODER_PIN_A, ENCODER_PIN_B, DEBOUNCE_TIME, p_menu_controller);
  
  // Set the pins of the shift register
  pinMode(SHIFT_REG_LATCH, OUTPUT);
  pinMode(SHIFT_REG_CLOCK, OUTPUT);
  pinMode(SHIFT_REG_DATA, INPUT);
  
  delay(10);
}

void loop() {
  
  if(menu_controller.get_redraw_display_flag() == true){
    // Change to a pointer to the currently selected menu.
    p_current_menu_page->draw(display);
    menu_controller.set_redraw_display_flag(false);  
  }
  
  //Serial.print(main_menu_txt[0][0]);


  // Set the latch pin to 1 to collect parallel data.
  digitalWrite(SHIFT_REG_LATCH, 1);
  delayMicroseconds(1);
  // Set the latch pin to to 0 to transmit data serially.
  digitalWrite(SHIFT_REG_LATCH, 0);
  // Collect the register as a byte.
  shift_reg_byte = shift_in(SHIFT_REG_DATA, SHIFT_REG_CLOCK);

  // Process the shift register buttons
  play_button.check_button_pressed(shift_reg_byte);
  stop_button.check_button_pressed(shift_reg_byte);
  song_1_button.check_button_pressed(shift_reg_byte);
  song_2_button.check_button_pressed(shift_reg_byte);
  song_3_button.check_button_pressed(shift_reg_byte);
  song_4_button.check_button_pressed(shift_reg_byte);
  back_button.check_button_pressed(shift_reg_byte);
  enter_button.check_button_pressed(shift_reg_byte);
  
  // Process the buttons connected directly to the microcontroller
  reconnect_button.check_button_pressed();
  power_button.check_button_pressed();
  access_switch.check_button_pressed();

  enter_button.set_callback_func(test_function);

  /*if(Serial.available() > 0){
    incomingByte = Serial.read();
    Serial.print("I received:");
    Serial.println(incomingByte, DEC);
  }*/

  /*while(Serial.available()) {
    Serial.readString();
    Serial.print("done");
  }*/

  // Get the current encoder position
  // Perhaps split this into two functions, track_position() and get_position()
  current_encoder_position = selection_encoder.track_position();

  // Has the value changed?
  if(current_encoder_position != last_encoder_position){
    // Print the value.
    Serial.println(current_encoder_position);
    // Update the last known value.
    last_encoder_position = current_encoder_position;
  }
}

byte shift_in(int incoming_data_pin, int incoming_clock_pin){
  int i;
  int temp = 0;
  //int pin_state;
  byte data_in = 0;

  // Set the clock pin to high in preparation for
  // reading the first value.
  digitalWrite(incoming_clock_pin, 1);

  for(i = 7; i >= 0; i--){
    // The data pin changes value to the next pin of the
    // shift register on every transition from HIGH to LOW
    digitalWrite(incoming_clock_pin, 0);
    delayMicroseconds(0.2);
    temp = digitalRead(incoming_data_pin);
    // If the temp value is HIGH then...
    if(temp){
      // ...set the corresponding bit to 1.
      // The OR operation allows us to maintain the state of the other bits.
      data_in = data_in | (1 << i);
    }
    // Set the clock pin to high in preparation for
    // reading the next value.
    digitalWrite(incoming_clock_pin, 1);
  }
  return data_in;
}

void print_bits(byte incoming_byte){
  for(int i = 7; i >= 0; i--){
    Serial.print(bitRead(incoming_byte,i));
  }
  Serial.println();
}

void test_function(){
  Serial.println(F("hello"));
}

void test_function_2(){
  Serial.println(F("sausages"));
}
