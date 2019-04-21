#include "Simple_Button.h"

Simple_Button::Simple_Button(int debounce_milliseconds){
  m_debounce_ms = debounce_milliseconds;
  m_last_event_time = 0;
  m_current_state = false;
}

Simple_Button::Simple_Button(int pin, int debounce_milliseconds){
  m_pin = pin;
  pinMode(m_pin, INPUT);
  m_debounce_ms = debounce_milliseconds;
  m_last_event_time = 0;
  m_current_state = false;
}
