#ifndef CONTROL_BUTTON
#define CONTROL_BUTTON
#include "Arduino.h"
#include "Menu_Controller.h"
#include "Simple_Button.h"

class Control_Button: public Simple_Button{
  protected:
    char m_serial_char;

  public:
    Control_Button(int debounce_milliseconds, char serial_char); 
    Control_Button(int pin, int debounce_milliseconds, char serial_char);    
    bool check_button_pressed();                                            // Call this to see if the button is being pressed
    void set_callback_func(void (*f)(Menu_Controller*));                    // Set the callback function, expects a pointer to a function which expects a pointer to a Menu_Controller
};
#endif
