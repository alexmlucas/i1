#ifndef SHIFT_REGISTER_BUTTON
#define SHIFT_REGISTER_BUTTON
#include "Arduino.h"                                  // Include the header file that defines INPUT and HIGH
#include "Simple_Button.h"                            // Include the parent class

class Shift_Register_Button: public Simple_Button{
  protected:
    int m_bit_position;
    
  public:
    Shift_Register_Button(int bit_position, int debounce_milliseconds, Menu_Controller *menu_controller);   // The constructor 
    bool check_button_pressed(byte &shift_register_reading);                                                // Call this to see if the button is being pressed   
};
#endif
