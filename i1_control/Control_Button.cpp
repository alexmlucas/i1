#include "Control_Button.h"

Control_Button::Control_Button(int debounce_milliseconds, int parameter_value):Simple_Button(debounce_milliseconds){
  m_parameter_value = parameter_value;
}

Control_Button::Control_Button(int pin, int debounce_milliseconds, int parameter_value):Simple_Button(pin, debounce_milliseconds){
  m_parameter_value = parameter_value;
}

void Control_Button::check_button_pressed(){
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
        m_parameter_container->set_parameter(m_parameter_struct, m_parameter_value);
      }
    }
  }
}

void Control_Button::configure_parameter(Parameter *parameter_struct, int parameter_value){
  m_parameter_struct = parameter_struct;
  m_parameter_value = parameter_value;
}

void Control_Button::set_parameter_container(Parameter_Container *parameter_container){
  m_parameter_container = parameter_container;
}
