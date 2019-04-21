#include "Shift_Register_Control_Button.h"

Shift_Register_Control_Button::Shift_Register_Control_Button(int bit_position, int debounce_milliseconds, char serial_char):Control_Button(debounce_milliseconds, serial_char){
  m_bit_position = bit_position;
}

bool Shift_Register_Control_Button::check_button_pressed(byte &shift_register_reading){
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
        Serial.println(m_serial_char);
      }
    }
  }
  return m_current_state;
}
