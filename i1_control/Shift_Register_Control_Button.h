#ifndef SHIFT_REGISTER_CONTROL_BUTTON
#define SHIFT_REGISTER_CONTROL_BUTTON
#include "Arduino.h"                                    // Include the header file that defines INPUT and HIGH
#include "Control_Button.h"                             // Include the parent class

class Shift_Register_Control_Button: public Control_Button{
  protected:
    int m_bit_position;
    
  public:
    Shift_Register_Control_Button(int bit_position, int debounce_milliseconds);
    bool check_button_pressed(byte &shift_register_reading);
};
#endif
