#include "Shift_Register_Button.h"

Shift_Register_Button::Shift_Register_Button(int bit_position, int debounce_milliseconds, const char &serial_handle){
  m_last_event_time = 0;
  //m_pin = pin;
  m_debounce_ms = debounce_milliseconds;
  m_current_state = false;
  m_bit_position = bit_position;
  m_serial_handle = serial_handle;
}

bool Shift_Register_Button::check_button_pressed(byte &shift_register_reading){
  boolean button_state;

  if(bitRead(shift_register_reading, m_bit_position) == HIGH){
    button_state = HIGH;
  } else{
    button_state = LOW;
  }

  // See if the button state has changed
  if(button_state != m_current_state){
    // See if enough time has passed to change the state.
    if((millis() - m_last_event_time) > m_debounce_ms){
      // It's okay to change state
      m_current_state = button_state;
      // Reset the timer
      m_last_event_time = millis();
      // If the button_state is HIGH, do something...
      if(button_state == HIGH){
        // send_serial is a inherited function.
        send_serial();
      }
    }
  }
  
  return m_current_state;
}
