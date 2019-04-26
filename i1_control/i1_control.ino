// Display includes
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Control includes
#include "Control_Button.h"
#include "Shift_Register_Control_Button.h"
#include "Shift_Register_Menu_Button.h"
#include "Simple_Encoder.h"
#include "Single_Led.h"
#include "Rg_Led.h"
#include "Rgb_Led.h"

// Menu includes
#include "Menu_Page.h"
#include "Main_Page.h"
#include "List_Page.h"
#include "Selection_Page.h"
#include "Value_Page.h"
#include "Splash_Page.h"
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

// Define LED pins
#define ZN_LED_R A9
#define ZN_LED_G A8
#define ZN_LED_B A7
#define WB_LED_R A3
#define WB_LED_G A2
#define PL_LED_G 10

// Define play button states
#define PLAYING 0
#define PAUSED 1
#define STOPPED 2

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

const static char song[] PROGMEM = "Song";
const static char guitar[] PROGMEM = "Guitar";
const char backing[] PROGMEM = "Backing";
const char master[] PROGMEM = "Master";
const static char zone[] PROGMEM = "Zone";
const static char mix_levels[] PROGMEM = "Mix Levels";
const char red_zone[] PROGMEM = "Red Zone";
const char green_zone[] PROGMEM = "Green Zone";
const char blue_zone[] PROGMEM = "Blue Zone";

const static char classic_rock[] PROGMEM = "Classic Rock";
const static char hard_rock[] PROGMEM = "Hard Rock";
const static char acoustic[] PROGMEM = "Acoustic";
const char scale[] PROGMEM = "Scale";
const char red_scale[] PROGMEM = "Red Scale";
const char green_scale[] PROGMEM = "Green Scale";
const char blue_scale[] PROGMEM = "Blue Scale";
const char root[] PROGMEM = "Root";
const char red_root[] PROGMEM = "Red Root";
const char green_root[] PROGMEM = "Green Root";
const char blue_root[] PROGMEM = "Blue Root";
const static char reconnecting[] PROGMEM = "Reconnecting";
const static char wristband[] PROGMEM = "wristband";
const static char please_wait[] PROGMEM = "please wait...";
const char sorry[] PROGMEM = "Sorry, I could";
const char not_connect[] PROGMEM = "not connect to";
const char the_wristband[] PROGMEM = "the wristband.";

//const char scale_param[] PROGMEM = "Major, Minor, Blues, Pent. Major, Pent. Minor, Major Chord, Minor Chord";
//const char root_param[] PROGMEM = "A, A#, B, C, C#, D, D#, E, F, F#, G, G#";

const char test_array[] PROGMEM = "test";
//const char flash_test PROGMEM = 'f';

// An array of constant pointers to constant chars?
const static char *const main_menu_txt[] PROGMEM = {song, guitar, zone, mix_levels};
const char *const guitar_menu_txt[] PROGMEM = {guitar, classic_rock, hard_rock, acoustic};
const char *const zone_menu_txt[] PROGMEM = {zone, red_zone, green_zone, blue_zone};
const char *const red_zone_menu_txt[] PROGMEM = {red_zone, scale, root};
const char *const green_zone_menu_txt[] PROGMEM = {green_zone, scale, root};
const char *const blue_zone_menu_txt[] PROGMEM = {blue_zone, scale, root};
const char *const red_scale_menu_txt[] PROGMEM = {red_scale};
const char *const green_scale_menu_txt[] PROGMEM = {green_scale};
const char *const blue_scale_menu_txt[] PROGMEM = {blue_scale};
const char *const red_root_menu_txt[] PROGMEM = {red_root};
const char *const green_root_menu_txt[] PROGMEM = {green_root};
const char *const blue_root_menu_txt[] PROGMEM = {blue_root};

const char *const mix_levels_menu_txt[] PROGMEM = {mix_levels, guitar, backing, master};
const char *const guitar_level_menu_txt[] PROGMEM = {guitar}; 
const char *const backing_level_menu_txt[] PROGMEM = {backing}; 
const char *const master_level_menu_txt[] PROGMEM = {master};

const static char *const reconnect_menu_txt[] PROGMEM = {reconnecting, wristband, please_wait};
const char *const connection_fail_menu_txt[] PROGMEM = {sorry, not_connect, the_wristband};

// const char* = a pointer to a constant char.
// char* const = a constant pointer to a char. (This pointer cannot be changed)
// const char* const = a constant pointer to a constant char (Nothing can be changed after declaration, therefore it can sit in program memory)
// const char* const my_array[] = a constant pointer to an array of constant chars (Nothing can be changed after declaration, therefore it can sit in program memory)

const char* const mix_levels_param_txt[] PROGMEM = {"0", "0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1"};
const char* const scales_param_txt[] PROGMEM = {"Major", "Minor", "Blues", "Pent. Major", "Pent. Minor", "Major Chord", "Minor Chord"};
const char* const root_param_txt[] PROGMEM = {"A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"};

// Define a variable to hold the data from the shift register
byte shift_reg_byte = 0;

// Create Simple_Encoder instance.
Simple_Encoder selection_encoder;

// A pointer to an array of constant pointers to constant chars.
const char *const *menu_text_pointer;

// Byte for storing incoming serial data.
int incoming_byte = 0;

// String representing the current menu location.
char current_menu_location[] = {""};

// Buffer for reading menu text.
char string_buffer[30];

// Read and monitior encoder position.
int current_encoder_position, last_encoder_position;

Menu_Controller menu_controller(MIN_CURSOR_VALUE, MAX_CURSOR_VALUE);      // Create an instance of Menu_Controller.
Parameter_Container parameter_container;                // Create an instance of Parameter_Container.
Parameter_Container *p_parameter_container;

// *** Initialise Menu_Page(s) ***
Main_Page main_menu(&menu_controller, &parameter_container);
Selection_Page guitar_menu(&menu_controller, &parameter_container);
List_Page zone_menu(&menu_controller, &parameter_container);
List_Page mix_levels_menu(&menu_controller, &parameter_container);
List_Page red_zone_menu(&menu_controller, &parameter_container);
List_Page green_zone_menu(&menu_controller, &parameter_container);
List_Page blue_zone_menu(&menu_controller, &parameter_container);
Value_Page red_scale_menu(&menu_controller, &parameter_container);
Value_Page red_root_menu(&menu_controller, &parameter_container);
Value_Page green_scale_menu(&menu_controller, &parameter_container);
Value_Page green_root_menu( &menu_controller, &parameter_container);
Value_Page blue_scale_menu(&menu_controller, &parameter_container);
Value_Page blue_root_menu(&menu_controller, &parameter_container);
Value_Page guitar_level_menu(&menu_controller, &parameter_container);
Value_Page backing_level_menu(&menu_controller, &parameter_container);
Value_Page master_level_menu(&menu_controller, &parameter_container);
Splash_Page reconnect_menu(&menu_controller, &parameter_container);
Splash_Page connection_fail_menu(&menu_controller, &parameter_container);

// *** Initialise Pointers to Sub Menu_Page(s) ***  
Menu_Page *p_main_sub_menus[] = {&guitar_menu, &zone_menu, &mix_levels_menu};                        
Menu_Page *p_zone_sub_menus[] = {&red_zone_menu, &green_zone_menu, &blue_zone_menu};
Menu_Page *p_red_zone_sub_menus[] = {&red_scale_menu, &red_root_menu};
Menu_Page *p_green_zone_sub_menus[] = {&green_scale_menu, &green_root_menu};
Menu_Page *p_blue_zone_sub_menus[] = {&blue_scale_menu, &blue_root_menu};    
Menu_Page *p_mix_levels_sub_menus[] = {&guitar_level_menu, &reconnect_menu, &connection_fail_menu};

Menu_Page *p_current_menu_page;                                           // Create a pointer to the currently selected menu page.
Menu_Page *p_previous_menu_page;                                          // Create a pointer to the previously selected menu page.

// *** Create Simple_Button instances ***
Control_Button reconnect_button(RECONNECT_BTN_PIN, DEBOUNCE_TIME, &menu_controller, &parameter_container, &parameter_container.m_reconnect, 0);
Control_Button power_button(POWER_BTN_PIN, DEBOUNCE_TIME, &menu_controller, &parameter_container, &parameter_container.m_power, 0);
Control_Button access_switch(ACCESS_SWT_PIN, DEBOUNCE_TIME, &menu_controller, &parameter_container, &parameter_container.m_selected_zone, 0);

// *** Create Shift_Register_Button instances ***
Shift_Register_Control_Button play_button(PLAY_BTN_BIT, DEBOUNCE_TIME, &menu_controller, &parameter_container, &parameter_container.m_play, 1);
Shift_Register_Control_Button stop_button(STOP_BTN_BIT, DEBOUNCE_TIME, &menu_controller, &parameter_container, &parameter_container.m_play, 0);
Shift_Register_Control_Button song_1_button(SONG_1_BTN_BIT, DEBOUNCE_TIME, &menu_controller, &parameter_container, &parameter_container.m_song, 0);
Shift_Register_Control_Button song_2_button(SONG_2_BTN_BIT, DEBOUNCE_TIME, &menu_controller, &parameter_container, &parameter_container.m_song, 1);
Shift_Register_Control_Button song_3_button(SONG_3_BTN_BIT, DEBOUNCE_TIME, &menu_controller, &parameter_container, &parameter_container.m_song, 2);
Shift_Register_Control_Button song_4_button(SONG_4_BTN_BIT, DEBOUNCE_TIME, &menu_controller, &parameter_container, &parameter_container.m_song, 3);

Shift_Register_Menu_Button back_button(BACK_BTN_BIT, DEBOUNCE_TIME, &menu_controller);
Shift_Register_Menu_Button enter_button(ENTER_BTN_BIT, DEBOUNCE_TIME, &menu_controller);

// *** Create Led instances ***
int zone_led_pins[] = {ZN_LED_R, ZN_LED_G, ZN_LED_B};
int wristband_led_pins[] = {WB_LED_R, WB_LED_G};

int RG_RED[] = {255, 0};
int RG_GREEN[] = {0, 255};
int RG_OFF[] = {0, 0};

int RGB_RED[] = {255, 0, 0};
int RGB_GREEN[] = {0, 255, 0};
int RGB_BLUE[] = {0, 0, 255};
int RGB_OFF[] = {0, 0, 0};

int *p_rgb_red = RGB_RED; 
int *p_rgb_blue = RGB_BLUE; 
bool FLASH_ALL[] = {true, true, true};

Single_Led play_led;
Rg_Led wristband_leds;
Rgb_Led zone_leds;

void setup() {
  // *** Assign menu text to Menu_Page(s) ***
  int text_size;
  text_size = sizeof(main_menu_txt)/sizeof(main_menu_txt[0]);                       // Main Menu
  main_menu.set_menu_text(main_menu_txt, text_size);
  text_size = sizeof(guitar_menu_txt)/sizeof(guitar_menu_txt[0]);                   // Guitar Menu
  guitar_menu.set_menu_text(guitar_menu_txt, text_size);
  text_size = sizeof(zone_menu_txt)/sizeof(zone_menu_txt[0]);                       // Zone Menu
  zone_menu.set_menu_text(zone_menu_txt, text_size);
  text_size = sizeof(mix_levels_menu_txt)/sizeof(mix_levels_menu_txt[0]);           // Mix Levels Menu
  mix_levels_menu.set_menu_text(mix_levels_menu_txt, text_size);
  text_size = sizeof(red_zone_menu_txt)/sizeof(red_zone_menu_txt[0]);               // Red Zone Menu
  red_zone_menu.set_menu_text(red_zone_menu_txt, text_size);
  text_size = sizeof(green_zone_menu_txt)/sizeof(green_zone_menu_txt[0]);           // Green Zone Menu
  green_zone_menu.set_menu_text(green_zone_menu_txt, text_size);
  text_size = sizeof(blue_zone_menu_txt)/sizeof(blue_zone_menu_txt[0]);             // Blue Zone Menu
  blue_zone_menu.set_menu_text(blue_zone_menu_txt, text_size);
  text_size = sizeof(red_scale_menu_txt)/sizeof(red_scale_menu_txt[0]);             // Red Scale Menu
  red_scale_menu.set_menu_text(red_scale_menu_txt, text_size); 
  text_size = sizeof(red_root_menu_txt)/sizeof(red_root_menu_txt[0]);               // Red Root Menu
  red_root_menu.set_menu_text(red_root_menu_txt, text_size);
  text_size = sizeof(green_scale_menu_txt)/sizeof(green_scale_menu_txt[0]);         // Green Scale Menu
  green_scale_menu.set_menu_text(green_scale_menu_txt, text_size);
  text_size = sizeof(green_root_menu_txt)/sizeof(green_root_menu_txt[0]);           // Green Root Menu
  green_root_menu.set_menu_text(green_root_menu_txt, text_size);
  text_size = sizeof(blue_scale_menu_txt)/sizeof(blue_scale_menu_txt[0]);           // Blue Scale Menu
  blue_scale_menu.set_menu_text(blue_scale_menu_txt, text_size);
  text_size = sizeof(blue_root_menu_txt)/sizeof(blue_root_menu_txt[0]);             // Blue Root Menu
  blue_root_menu.set_menu_text(blue_root_menu_txt, text_size);
  text_size = sizeof(guitar_level_menu_txt)/sizeof(guitar_level_menu_txt[0]);       // Guitar Level Menu
  guitar_level_menu.set_menu_text(guitar_level_menu_txt, text_size);
  text_size = sizeof(backing_level_menu_txt)/sizeof(backing_level_menu_txt[0]);     // Guitar Backing Menu
  backing_level_menu.set_menu_text(backing_level_menu_txt, text_size);
  text_size = sizeof(master_level_menu_txt)/sizeof(master_level_menu_txt[0]);       // Master Level Menu
  master_level_menu.set_menu_text(master_level_menu_txt, text_size);
  text_size = sizeof(reconnect_menu_txt)/sizeof(reconnect_menu_txt[0]);             // Reconnect Menu
  reconnect_menu.set_menu_text(reconnect_menu_txt, text_size);
  text_size = sizeof(connection_fail_menu_txt)/sizeof(connection_fail_menu_txt[0]); // Connection Fail Menu
  connection_fail_menu.set_menu_text(connection_fail_menu_txt, text_size);

  // *** Assign parameter text to Menu_Page(s) ***
  text_size = sizeof(scales_param_txt)/sizeof(scales_param_txt[0]);                 // Scales parameter text
  red_scale_menu.set_parameter_text(scales_param_txt, text_size);
  green_scale_menu.set_parameter_text(scales_param_txt, text_size);
  blue_scale_menu.set_parameter_text(scales_param_txt, text_size);
  text_size = sizeof(root_param_txt)/sizeof(root_param_txt[0]);                     // Root parameter text
  red_root_menu.set_parameter_text(root_param_txt, text_size);
  green_root_menu.set_parameter_text(root_param_txt, text_size);
  blue_root_menu.set_parameter_text(root_param_txt, text_size);
  text_size = sizeof(mix_levels_param_txt)/sizeof(mix_levels_param_txt[0]);         // Mix Levels parameter text
  guitar_level_menu.set_parameter_text(mix_levels_param_txt, text_size);
  backing_level_menu.set_parameter_text(mix_levels_param_txt, text_size);
  master_level_menu.set_parameter_text(mix_levels_param_txt, text_size);

  // *** Assign parameter structs to Menu_Page(s) ***
  main_menu.set_parameter_struct(&parameter_container.m_song);
  guitar_menu.set_parameter_struct(&parameter_container.m_guitar);
  red_scale_menu.set_parameter_struct(&parameter_container.m_red_scale);
  red_root_menu.set_parameter_struct(&parameter_container.m_red_root);
  green_scale_menu.set_parameter_struct(&parameter_container.m_green_scale);
  green_root_menu.set_parameter_struct(&parameter_container.m_green_root);
  blue_scale_menu.set_parameter_struct(&parameter_container.m_blue_scale);
  blue_root_menu.set_parameter_struct(&parameter_container.m_blue_root);
  guitar_level_menu.set_parameter_struct(&parameter_container.m_guitar_level);
  backing_level_menu.set_parameter_struct(&parameter_container.m_backing_level);
  master_level_menu.set_parameter_struct(&parameter_container.m_master_level);

  menu_controller.set_currently_selected_menu(&main_menu);                // Setting the main_menu as the Menu_Page currently selected

  // *** Build the menu system ***
  main_menu.set_sub_menus(p_main_sub_menus);                              // Add sub Menu_Page(s) to Menu_Page(s)
  zone_menu.set_sub_menus(p_zone_sub_menus);
  red_zone_menu.set_sub_menus(p_red_zone_sub_menus);
  green_zone_menu.set_sub_menus(p_green_zone_sub_menus);
  blue_zone_menu.set_sub_menus(p_blue_zone_sub_menus);
  mix_levels_menu.set_sub_menus(p_mix_levels_sub_menus);
  
  guitar_menu.set_previous_menu(&main_menu);                              // Make the Menu_Page(s) aware of their parents. 
  zone_menu.set_previous_menu(&main_menu);                                
  mix_levels_menu.set_previous_menu(&main_menu);
  red_zone_menu.set_previous_menu(&zone_menu);                                                    
  green_zone_menu.set_previous_menu(&zone_menu);  
  blue_zone_menu.set_previous_menu(&zone_menu);  
  guitar_level_menu.set_previous_menu(&mix_levels_menu);
  backing_level_menu.set_previous_menu(&mix_levels_menu);
  master_level_menu.set_previous_menu(&mix_levels_menu);
  red_scale_menu.set_previous_menu(&red_zone_menu);
  red_root_menu.set_previous_menu(&red_zone_menu);
  green_scale_menu.set_previous_menu(&red_zone_menu);
  green_root_menu.set_previous_menu(&red_zone_menu);
  blue_scale_menu.set_previous_menu(&red_zone_menu);
  blue_root_menu.set_previous_menu(&red_zone_menu);

  Serial.begin(9600);                                                                           // Begin serial
  delay(500);                                                                                   // Wait for the serial stream to get going.

  play_led.set_pinout(PL_LED_G);
  wristband_leds.set_pinout(wristband_led_pins);
  zone_leds.set_pinout(zone_led_pins);
  
  play_led.set_on(false);
  wristband_leds.set_colour(RG_RED);
  wristband_leds.set_flashing(true);
  zone_leds.set_colour(p_rgb_blue);        // A hack until parameter reading is implemented.


  // *** Configure the buttons ***
  play_button.set_led(&play_led);
  stop_button.set_led(&play_led);
  access_switch.set_led(&zone_leds);
  
  enter_button.set_callback_func(enter_pressed);                                                // Set button callback functions
  back_button.set_callback_func(back_pressed);
  play_button.set_callback_func(play_pressed);
  stop_button.set_callback_func(stop_pressed);
  access_switch.set_callback_func(access_switch_pressed);

  song_1_button.m_redraw_display = true;
  song_2_button.m_redraw_display = true;
  song_3_button.m_redraw_display = true;
  song_4_button.m_redraw_display = true;

  delay(1500);
  //play_led.set_flashing(true);
  //wristband_leds.set_flashing(true);
  //zone_leds.set_flashing(true);
  
  selection_encoder.initialise(ENCODER_PIN_A, ENCODER_PIN_B, DEBOUNCE_TIME, &menu_controller);  // Initialise the encoder
  
  pinMode(SHIFT_REG_LATCH, OUTPUT);                                                             // Set the pins of the shift register
  pinMode(SHIFT_REG_CLOCK, OUTPUT);
  pinMode(SHIFT_REG_DATA, INPUT);
  
  display.begin(SSD1306_SWITCHCAPVCC, 0x3D);                                                    // Initialise the display with the 12C address 0x3D
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.clearDisplay();
  display.display();
 
  delay(10);                                                                                    // Pause again before we get going.
  
  // an array of pointers to constant chars.
  // unusual that the addresses do not need to be passed in. Perhaps this is a peculiarity...
  // ...of char arrays and the fact that we're declaring and initialising the array of pointers to const chars at the same time.
  // const char* test_array[] = {test, test2};

}

void loop() {
  
  if(menu_controller.get_redraw_display_flag() == true){
    // Change to a pointer to the currently selected menu.
    p_current_menu_page = (Menu_Page*)menu_controller.get_currently_selected_menu();
    p_current_menu_page->draw(display);
    menu_controller.set_redraw_display_flag(false);  
  }
  
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

  // Process the leds that need to flash.
  play_led.update_flashing();
  wristband_leds.update_flashing();
 
  if(Serial.available() > 0){
    incoming_byte = Serial.read();
    Serial.print("I received:");
    Serial.println(incoming_byte, DEC);

    switch(incoming_byte){
      case 49: 
        //wristband_not_connected_led.set_flashing(true);
        //wristband_connected_led.set_on(false);
        break;
      case 50:
        //wristband_not_connected_led.set_flashing(false);
        //wristband_not_connected_led.set_on(false);
        //wristband_connected_led.set_on(true);
        break;
      case 51:
        //play_led.set_flashing(false); // move these functions to the Simple Led class?
        //play_led.set_on(true);
        break;
      case 52:
        //play_led.set_flashing(false);
        //play_led.set_on(false);
        break;
      case 53:
        //play_led.set_flashing(true);
      case 54:
        // Attempting to connect to wristband
        p_previous_menu_page = (Menu_Page*)menu_controller.get_currently_selected_menu();       // Store a reference to the currently displayed menu.
        menu_controller.set_currently_selected_menu(&reconnect_menu);                           // Switch to splash menu.
        //zone_leds.set_colour(BLUE);
        break; 
      case 55:
        // Successfully connected to wristband.
        menu_controller.set_currently_selected_menu(p_previous_menu_page);
        wristband_leds.set_flashing(false);
        wristband_leds.set_colour(RG_GREEN);
        break;
      case 57:
        // Connection to wristband unsuccessful.
        menu_controller.set_currently_selected_menu(&connection_fail_menu);
        break;
    }
  }

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

void enter_pressed(Menu_Controller* p_menu_controller){                                // Function expects a pointer to a Menu_Controller.
  Menu_Page *m_menu = (Menu_Page*)p_menu_controller->m_currently_selected_menu;        // Create local pointer to the currently selected Menu_Page, via the Menu_Controller pointer.
  
  if(m_menu->m_enter_enabled){                                                         // if the currently selected menu has an on_enter() function...
    m_menu->on_enter();                                                                // ... call it.
  }                                                                   
}

void back_pressed(Menu_Controller* p_menu_controller){                                 // Function expects a pointer to a Menu_Controller.
  Menu_Page *m_menu = (Menu_Page*)p_menu_controller->m_currently_selected_menu;        // Create local pointer to the currently selected Menu_Page, via the Menu_Controller pointer.
  
  if(m_menu->m_back_enabled){                                                          // if the currently selected menu has an on_enter() function...
    m_menu->on_back();                                                                 // ... call it.
  }                                                      
}

/*void set_red_zone_on(){
  analogWrite(ZN_LED_R, 255);
  analogWrite(ZN_LED_G, 0);
  analogWrite(ZN_LED_B, 0);
}

void set_green_zone_on(){
  analogWrite(ZN_LED_R, 0);
  analogWrite(ZN_LED_G, 255);
  analogWrite(ZN_LED_B, 0);
}

void set_blue_zone_on(){
  analogWrite(ZN_LED_R, 0);
  analogWrite(ZN_LED_G, 0);
  analogWrite(ZN_LED_B, 255);
}

void set_play_on(){
  analogWrite(PL_LED_G, 255);
}

void set_play_off(){
  analogWrite(PL_LED_G, 0);
}*/

void play_pressed(Single_Led *led, Parameter_Container *parameter_container, Parameter *parameter_struct){

  Serial.println("There is a callback function.");
  Serial.print("The address of the led is: ");
  Serial.println((int)led);

  Serial.print("The address of the parameter_container is: ");
  Serial.println((int)parameter_container);

  Serial.print("The address of the parameter_struct is: ");
  Serial.println((int)parameter_struct);
          
  switch(parameter_struct->value){
    case 0:
      parameter_container->set_parameter(parameter_struct, 1);        // Playback is currently stopped, so start it.
      led->set_on(true);                                              // Update the led
      break;
    case 1:
      parameter_container->set_parameter(parameter_struct, 2);        // Song is playing already, so pause it.
      led->set_flashing(true);                                        // Update the led

      break;
    case 2:
      parameter_container->set_parameter(parameter_struct, 1);        // Song is paused, so commence playback.
      led->set_on(true);                                              // Update the led
      break;
  }
}

void stop_pressed(Single_Led *led, Parameter_Container *parameter_container, Parameter *parameter_struct){
  if(parameter_struct->value){
    parameter_container->set_parameter(parameter_struct, 0);          // Currently playing the song, so stop it.
    led->set_on(false);                                               
  }
}

void access_switch_pressed(Single_Led *led, Parameter_Container *parameter_container, Parameter *parameter_struct){
  Rgb_Led *rgb_led = (Rgb_Led*)led;        // Create local pointer to the currently selected Menu_Page, via the Menu_Controller pointer.

  switch(parameter_struct->value){
    case 0:
      parameter_container->set_parameter(parameter_struct, 1);        // Increment parameter value
      rgb_led->set_colour(RGB_GREEN);                                 // Update the led
      break;
    case 1:
      parameter_container->set_parameter(parameter_struct, 2);        // Increment parameter value
      rgb_led->set_colour(RGB_BLUE);                                  // Update the led
      break;
    case 2:
      parameter_container->set_parameter(parameter_struct, 0);        // Reset parameter value to 0
      rgb_led->set_colour(RGB_RED);                                   // Update the led
      break;
  }
}

/*void set_wristband_error(){
  analogWrite(WB_LED_R, 255);
}

void set_wristband_good(){
  analogWrite(WB_LED_G, 255);
}*/
