#include "Simple_Button.h"

Simple_Button::Simple_Button(){
  // Default constructor
}

Simple_Button::Simple_Button(int pin, int debounce_milliseconds,const char &serial_handle){
  m_last_event_time = 0;
  m_pin = pin;
  m_debounce_ms = debounce_milliseconds;
  m_current_state = false;
  m_serial_handle = serial_handle;
  pinMode(m_pin, INPUT);
}

bool Simple_Button::check_button_pressed(){
  boolean button_state;

  if(digitalRead(m_pin) == HIGH){
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
        send_serial();
        if(callback_function != NULL){
          Serial.println("a callback function exisits");
        }
      }
    }
  }
  return m_current_state;
}

void Simple_Button::set_callback_func(void (*f)()){
  callback_function = f;
}

void Simple_Button::send_serial(){
  Serial.println(m_serial_handle);
  //Serial.println("test");
}
