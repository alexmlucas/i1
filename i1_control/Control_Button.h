#ifndef CONTROL_BUTTON
#define CONTROL_BUTTON
#include "Arduino.h"
#include "Menu_Controller.h"
#include "Simple_Button.h"
#include "Parameter.h"
#include "Parameter_Container.h"

class Control_Button: public Simple_Button{
  protected:
    int m_parameter_value;
    Parameter *m_parameter_struct;
    Parameter_Container *m_parameter_container;

  public:
    Control_Button(int debounce_milliseconds, int parameter_value);                // Present to allow base class to be initialised from shift_register button, which doesn't have a pin.
    Control_Button(int pin, int debounce_milliseconds, int parameter_value);    
    void check_button_pressed();                                       
    void configure_parameter(Parameter *parameter, int parameter_value);
    void set_parameter_container(Parameter_Container *parameter_container);
};
#endif
