#include "ButtonDebounce.h"
#include "Simple_Button.h"
#include "Simple_Encoder.h"

// Create variables for tracking last states.
byte last_shift_reg_state;
int last_reconnect_btn_state;
int last_encoder_a_state;
int last_power_btn_state;
int last_switch_state;

// Create variables for reading current states.
byte current_shift_reg_state;
int current_reconnect_btn_state;
int current_power_btn_state;
int current_switch_state;
int current_encoder_a_state;

// Create variables for recording debounce time.
unsigned long reconnect_last_debounce_time = 0;
unsigned long power_last_debounce_time = 0;
unsigned long switch_last_debounce_time = 0;
unsigned long encoder_a_last_debounce_time = 0;

unsigned long debounce_delay = 50; 

// Create timers for debouncing.
long timer_1 = millis();

// Define the button pins
const int RECONNECT_BTN = 12; 
const int POWER_BTN = 13;

// Define access switch pin
const int SWITCH = A1; 

// Define the encoder pins
const int ENCODER_PIN_A = 2;
const int ENCODER_PIN_B = 4; 

// Instantiate the debouncer
Debouncer shift_reg_debounced(0b00000000);

// Define the shift register pins.
const int SHIFT_REG_LATCH = 8;
const int SHIFT_REG_DATA = A3;
const int SHIFT_REG_CLOCK = 7;

// define a variable to hold the data from the shift register
byte shift_reg_byte = 0; // 01001000

Simple_Button reconnect_button(POWER_BTN, 50);
Simple_Encoder my_encoder;

int last_encoder_position;

void setup() {
  Serial.begin(9600);



  
  my_encoder.initialise(ENCODER_PIN_A, ENCODER_PIN_B, 50);
  reconnect_button.set_callback_func(test_function);
 
  pinMode(SHIFT_REG_LATCH, OUTPUT);
  pinMode(SHIFT_REG_CLOCK, OUTPUT);
  pinMode(SHIFT_REG_DATA, INPUT);

  pinMode(RECONNECT_BTN, INPUT);
  pinMode(POWER_BTN, INPUT);
  pinMode(ENCODER_PIN_A, INPUT_PULLUP);
  pinMode(ENCODER_PIN_B, INPUT_PULLUP);
  pinMode(SWITCH, INPUT);
}

void loop() {

  reconnect_button.check_button_pressed();
  int encoder_position = my_encoder.track_position();
  if (encoder_position != last_encoder_position){
    Serial.println(encoder_position);
    last_encoder_position = encoder_position;
  }

  //reconnect_button.callback_function();

  // Read the state of the buttons, switch and encoder.
  int reconnect_btn_reading = digitalRead(RECONNECT_BTN);
  int power_btn_reading = digitalRead(POWER_BTN);
  int switch_reading = digitalRead(SWITCH);
  int encoder_a_reading = digitalRead(ENCODER_PIN_A);

  // If any of the above inputs have changed due to noise or user activity, reset the appropriate timer.
  if(reconnect_btn_reading != last_reconnect_btn_state){
    reconnect_last_debounce_time = millis();
  }

  if(power_btn_reading != last_power_btn_state){
    power_last_debounce_time = millis();
  }

  if(switch_reading != last_switch_state){
    switch_last_debounce_time = millis();
  }

  if(encoder_a_reading != last_encoder_a_state){
    encoder_a_last_debounce_time = millis();
  }

  // If any input readings have been there longer than the debounce delay, process the input.
  if ((millis() - reconnect_last_debounce_time) > debounce_delay){
    // Has the state changed?
    
    if (reconnect_btn_reading != current_reconnect_btn_state){
      // Update the current value
      current_reconnect_btn_state = reconnect_btn_reading; 
      
      // Do something if the state has changed to HIGH.
      if (current_reconnect_btn_state == HIGH){
        Serial.println("Something has happened");
      } 
    }
  }

  // Update the last state.
  last_reconnect_btn_state = reconnect_btn_reading;

  // Read shift register pin states every 4ms
  if(millis() - timer_1 > 4){
    // Set the latch pin to 1 to collect parallel data.
    digitalWrite(SHIFT_REG_LATCH, 1);
    delayMicroseconds(1);
    // Set the latch pin to to 0 to transmit data serially.
    digitalWrite(SHIFT_REG_LATCH, 0);
    // Collect the register as a byte.
    shift_reg_byte = shift_in(SHIFT_REG_DATA, SHIFT_REG_CLOCK);
    // Process the byte
    shift_reg_debounced.ButtonProcess(shift_reg_byte);
    timer_1 = millis();
  }

  last_shift_reg_state = current_shift_reg_state;

  // Read all 8 bits
  current_shift_reg_state = shift_reg_debounced.ButtonCurrent(0b11111111);

  if(last_shift_reg_state ^ current_shift_reg_state){
    // The state of the byte has changed
    print_bits(current_shift_reg_state);
  }
}

byte shift_in(int incoming_data_pin, int incoming_clock_pin){
  int i;
  int temp = 0;
  int pin_state;
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
  Serial.println("hello");
}
