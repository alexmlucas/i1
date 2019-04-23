#include "Simple_Button.h"

Simple_Button::Simple_Button(int pin, int debounce_milliseconds, Menu_Controller *menu_controller){
  m_last_event_time = 0;
  m_pin = pin;
  m_debounce_ms = debounce_milliseconds;
  m_current_state = false;
  pinMode(m_pin, INPUT);
  m_menu_controller = menu_controller;
}

bool Simple_Button::check_button_pressed(){
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
        if(callback_function != NULL){                          // ... If there's a callback function...
          callback_function(m_menu_controller);                 // ... call it!
        }
      }
    }
  }
  return m_current_state;
}

void Simple_Button::set_callback_func(void (*f)(Menu_Controller*)){
  callback_function = f;
}
