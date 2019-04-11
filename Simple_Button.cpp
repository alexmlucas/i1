#include "Simple_Button.h"

Simple_Button::Simple_Button(int pin, int debounce_milliseconds){
  m_last_event_time = 0;
  m_pin = pin;
  m_debounce_ms = debounce_milliseconds;
  m_current_state = false;
}

void Simple_Button::initialise(int pin, int debounce_milliseconds){
  m_pin = pin;
  m_debounce_ms = debounce_milliseconds;
  pinMode(m_pin, INPUT);
}

bool Simple_Button::check_button_pressed(){
  boolean button_state;

  if(digitalRead(m_pin) == HIGH){
    button_state = true;
  } else{
    button_state = false;
  }

  // See if the button state has changed
  if(button_state != m_current_state){
    // See if enough time has passed to change the state.
    if((millis() - m_last_event_time) > m_debounce_ms){
      // It's okay to change state
      m_current_state = button_state;
      // Reset the timer
      m_last_event_time = millis();
      // If the button_state is HIGH, call the callback function
      if(button_state == HIGH){
        callback_function();
      }
    }
  }
  
  return m_current_state;
}

void Simple_Button::set_callback_func(void (*f)()){
  callback_function = f;
}
