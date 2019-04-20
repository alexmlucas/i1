#include "Shift_Register_Button.h"

Shift_Register_Button::Shift_Register_Button(int bit_position, int debounce_milliseconds, Menu_Controller *menu_controller):Simple_Button(bit_position, debounce_milliseconds, menu_controller){
  m_last_event_time = 0;
  m_debounce_ms = debounce_milliseconds;
  m_current_state = false;
  m_bit_position = bit_position;
}

bool Shift_Register_Button::check_button_pressed(byte &shift_register_reading){
  boolean button_state;

  if(bitRead(shift_register_reading, m_bit_position) == HIGH){
    button_state = HIGH;
  } else{
    button_state = LOW;
  }

 if(button_state != m_current_state){                          // Has the button changed state?
    if((millis() - m_last_event_time) > m_debounce_ms){         // If the debounce time has been exceeded...
      m_current_state = button_state;                           // ... change state.
      m_last_event_time = millis();                             // Reset the timer ready for the next iteration.
      if(button_state == HIGH){                                 // If the button is HIGH...
        if(callback_function != NULL){                          // ... If there's a callback function...
          callback_function(m_menu_controller);                 // ... call it!
        }
      }
    }
  }
  return m_current_state;
}
