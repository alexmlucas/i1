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
    // ... read the current value of pin_B.
    // If the value of pin_B is LOW, a clockwise rotation has occured.
    if(digitalRead(m_pin_B) == LOW){
      if(m_menu_controller->get_cursor_position() < m_menu_controller->get_cursor_max_value()){
        m_menu_controller->increment_cursor_position();
      }
    } else {
      //...otherwise an anit-clockwise rotation has occured.
      if(m_menu_controller->get_cursor_position() > m_menu_controller->get_cursor_min_value()){
        m_menu_controller->decrement_cursor_position();
      }
    }

    // Update the last event time.
    m_last_event_time = current_time;
  }

  // Record the last known value ready for the next iteration.
   m_encoder_A_last = pin_A_value;
   return m_encoder_position;
}
