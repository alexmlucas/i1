// Display includes
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

// Button includes
#include "Control_Button.h"
#include "Shift_Register_Control_Button.h"
#include "Shift_Register_Menu_Button.h"

#include "Simple_Encoder.h"

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
int incomingByte = 0;

// String representing the current menu location.
char current_menu_location[] = {""};

// Buffer for reading menu text.
char string_buffer[30];

// Read and monitior encoder position.
int current_encoder_position, last_encoder_position;

Menu_Controller menu_controller(MIN_CURSOR_VALUE, MAX_CURSOR_VALUE);      // Create an instance of Menu_Controller.
Parameter_Container parameter_container;                                  // Create an instance of Parameter_Container.

// *** Initialise Menu_Page(s) ***
Main_Page main_menu(&menu_controller, &parameter_container);
Selection_Page guitar_menu(&menu_controller, &parameter_container, &parameter_container.m_selected_guitar);
List_Page zone_menu(&menu_controller, &parameter_container);
List_Page mix_levels_menu(&menu_controller, &parameter_container);
List_Page red_zone_menu(&menu_controller, &parameter_container);
List_Page green_zone_menu(&menu_controller, &parameter_container);
List_Page blue_zone_menu(&menu_controller, &parameter_container);
Value_Page red_scale_menu(&menu_controller, &parameter_container, &parameter_container.m_red_scale);
Value_Page red_root_menu(&menu_controller, &parameter_container, &parameter_container.m_red_root);
Value_Page green_scale_menu(&menu_controller, &parameter_container, &parameter_container.m_green_scale);
Value_Page green_root_menu( &menu_controller, &parameter_container, &parameter_container.m_green_root);
Value_Page blue_scale_menu(&menu_controller, &parameter_container, &parameter_container.m_blue_scale);
Value_Page blue_root_menu(&menu_controller, &parameter_container, &parameter_container.m_blue_root);
Value_Page guitar_level_menu(&menu_controller, &parameter_container, &parameter_container.m_guitar_level);
Value_Page backing_level_menu(&menu_controller, &parameter_container, &parameter_container.m_backing_level);
Value_Page master_level_menu(&menu_controller, &parameter_container, &parameter_container.m_master_level);
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

// *** Create Simple_Button instances ***
Control_Button reconnect_button(RECONNECT_BTN_PIN, DEBOUNCE_TIME, 'a');
Control_Button power_button(POWER_BTN_PIN, DEBOUNCE_TIME, 'b');
Control_Button access_switch(ACCESS_SWT_PIN, DEBOUNCE_TIME, 'c');

// *** Create Shift_Register_Button instances ***
Shift_Register_Control_Button play_button(PLAY_BTN_BIT, DEBOUNCE_TIME, 'd');
Shift_Register_Control_Button stop_button(STOP_BTN_BIT, DEBOUNCE_TIME, 'e');
Shift_Register_Control_Button song_1_button(SONG_1_BTN_BIT, DEBOUNCE_TIME, 'f');
Shift_Register_Control_Button song_2_button(SONG_2_BTN_BIT, DEBOUNCE_TIME, 'g');
Shift_Register_Control_Button song_3_button(SONG_3_BTN_BIT, DEBOUNCE_TIME, 'h');
Shift_Register_Control_Button song_4_button(SONG_4_BTN_BIT, DEBOUNCE_TIME, 'i');

Shift_Register_Menu_Button back_button(BACK_BTN_BIT, DEBOUNCE_TIME, &menu_controller);
Shift_Register_Menu_Button enter_button(ENTER_BTN_BIT, DEBOUNCE_TIME, &menu_controller);

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

  enter_button.set_callback_func(enter_pressed);                                                // Set button callback functions
  back_button.set_callback_func(back_pressed);

  Serial.begin(9600);                                                                           // Begin serial
  delay(500);                                                                                   // Wait for the serial stream to get going.

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
  //Serial.println("Hello");

  // print the size of a pointer divided by the number of pointers.
  // Serial.println(sizeof(scales_param)/sizeof(scales_param[0]));

  char test[] = "hey";
  char test2[] = "f";
  char test3 = 'g';
  char *test4;
  test4 = &test3;
  //Serial.println(sizeof(test4));

  // an array of pointers to constant chars.
  // unusual that the addresses do not need to be passed in. Perhaps this is a peculiarity...
  // ...of char arrays and the fact that we're declaring and initialising the array of pointers to const chars at the same time.
  const char* test_array[] = {test, test2};

  // Serial.println(sizeof(test_array)/sizeof(test_array[1]));
  Serial.println(sizeof(main_menu_txt));
  Serial.print("The address of the text is: ");
  Serial.println((int)&main_menu_txt);
  
  function_test(main_menu_txt);
  function_test(reconnect_menu_txt);
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

void send_serial(char handle){
  Serial.println(handle);

}

void function_test(const char *const menu_text[]){
  Serial.println((int)pgm_read_ptr(&(menu_text)));   
  //Serial.println(sizeof(pgm_read_ptr(menu_text)));
  Serial.println(sizeof(menu_text));
  //strcpy_P(string_buffer, (char *)pgm_read_word(&(m_menu_text[i])));
  //Serial.println(sizeof(menu_text)/sizeof(menu_text[1]));                                                          
}
