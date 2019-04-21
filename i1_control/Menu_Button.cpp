#include "Menu_Button.h"

Menu_Button::Menu_Button(int debounce_milliseconds, Menu_Controller *menu_controller):Simple_Button(debounce_milliseconds){
  m_menu_controller = menu_controller;
}

Menu_Button::Menu_Button(int pin, int debounce_milliseconds, Menu_Controller *menu_controller):Simple_Button(pin, debounce_milliseconds){
  m_menu_controller = menu_controller;
}

bool Menu_Button::check_button_pressed(){
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

void Menu_Button::set_callback_func(void (*f)(Menu_Controller*)){
  callback_function = f;
}
