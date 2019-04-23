#ifndef SIMPLE_BUTTON
#define SIMPLE_BUTTON
#include "Arduino.h"
#include "Menu_Controller.h"
#include "Menu_Page.h"

class Simple_Button{
  protected:
    int m_pin;                                        // The digital pin the button is connected to.
    int m_debounce_ms;                                // The number of milliseconds for debouncing
    unsigned long m_last_event_time;                  // Timestamp of the last event
    boolean m_current_state;                          // The current state of the button
  public:
    Simple_Button(int debounce_milliseconds);         // Present to allow base class to be initialised from shift_register button, which doesn't have a pin.
    Simple_Button(int pin, int debounce_milliseconds);  
};
#endif
