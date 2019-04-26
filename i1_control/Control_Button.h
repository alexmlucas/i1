#ifndef CONTROL_BUTTON
#define CONTROL_BUTTON
#include "Arduino.h"
#include "Simple_Button.h"
#include "Parameter.h"
#include "Parameter_Container.h"
#include "Menu_Controller.h"
#include "Single_Led.h"

class Control_Button: public Simple_Button{
  protected:
    Menu_Controller *m_menu_controller;
    Parameter_Container *m_parameter_container;
    Parameter *m_parameter_struct;
    int m_parameter_value;
    Single_Led *m_led;
    void (*callback_function)(Single_Led *, Parameter_Container *parameter_container, Parameter *parameter_struct);

  public:
    bool m_redraw_display;
    bool m_update_leds;
    Control_Button(int debounce_milliseconds);                // Present to allow base class to be initialised from shift_register button, which doesn't have a pin.
    Control_Button(int pin, int debounce_milliseconds, Menu_Controller *menu_controller, Parameter_Container *parameter_container, Parameter *parameter_struct, int parameter_value);   
    void check_button_pressed();
    void set_led(Single_Led *led);
    void set_callback_func(void (*f)(Single_Led *, Parameter_Container *parameter_container, Parameter *parameter_struct));
                                   
};
#endif
