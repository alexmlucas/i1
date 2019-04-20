#include "Simple_Encoder.h"

Simple_Encoder::Simple_Encoder(){
  // Set default values
}

void Simple_Encoder::initialise(int pin_A, int pin_B, int debounce_milliseconds, Menu_Controller *menu_controller){
  m_pin_A = pin_A;
  m_pin_B = pin_B;
  m_debounce_ms = debounce_milliseconds;
  m_last_event_time = 0;
  m_encoder_position = 0;
  m_encoder_max = 3;
  m_encoder_min = 0;
  m_encoder_A_last = HIGH;

  pinMode(m_pin_A, INPUT_PULLUP);
  pinMode(m_pin_B, INPUT_PULLUP); 

  // Both pointers now point to the same memory address.
  m_menu_controller = menu_controller;
}

int Simple_Encoder::track_position(){
  
  // Read the current value from pin_A 
  bool pin_A_value = digitalRead(m_pin_A);
  // Get the current time.
  unsigned long current_time = millis();
  // Get the time since the last event.
  unsigned long time_between_events = current_time - m_last_event_time;

  // If there has been a transition from HIGH to LOW and the debounce time has been exceeded...
  if((m_encoder_A_last == HIGH) && (pin_A_value == LOW) && time_between_events > m_debounce_ms){
    
    Menu_Page *currently_selected_menu = (Menu_Page*)m_menu_controller->m_currently_selected_menu;  // Create a local pointer to the currently selected Menu_Page.
    
    if(currently_selected_menu->m_encoder_enabled){                                                 // If the currently selected menu has the encoder function enabled....
      uint8_t pin_b_value = digitalRead(m_pin_B);                                                       // Get the value of pin B.
      currently_selected_menu->on_encoder(&pin_b_value);                                            // Pass on the pin B value.
    }
    
    // Update the last event time.
    m_last_event_time = current_time;
  }

  // Record the last known value ready for the next iteration.
   m_encoder_A_last = pin_A_value;
   return m_encoder_position;
}
