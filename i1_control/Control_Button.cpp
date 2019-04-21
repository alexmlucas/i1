#include "Control_Button.h"

Control_Button::Control_Button(int debounce_milliseconds, char serial_char):Simple_Button(debounce_milliseconds){
  m_serial_char = serial_char;
}

Control_Button::Control_Button(int pin, int debounce_milliseconds, char serial_char):Simple_Button(pin, debounce_milliseconds){
  m_serial_char = serial_char;
}

bool Control_Button::check_button_pressed(){
  boolean button_state;

  if(digitalRead(m_pin) == HIGH){
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
