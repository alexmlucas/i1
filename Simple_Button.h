#ifndef SIMPLE_BUTTON
#define SIMPLE_BUTTON
#include "Arduino.h"                                  // Include the header file that defines INPUT and HIGH

class Simple_Button{
  private:
    int m_pin;                                        // The digital pin the button is connected to.
    int m_debounce_ms;                                // The number of milliseconds for debouncing
    unsigned long m_last_event_time;                  // Timestamp of the last event
    boolean m_current_state;                          // The current state of the button

  public:
    Simple_Button(int pin, int debounce_milliseconds);// The constructor 
    void initialise(int pin, int debounce_milliseconds);    // A helper method to set the input pin and number of milliseconds for debounce
    bool check_button_pressed();                      // Call this to see if the button is being pressed
    bool check_button_pressed(unsigned long ticks);    // Use this method when the millis() function is disabled.
    void set_callback_func(void (*f)());
    void (*callback_function)();
    
};
#endif
