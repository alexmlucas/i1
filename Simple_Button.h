#ifndef SIMPLE_BUTTON
#define SIMPLE_BUTTON
#include "Arduino.h"                                  // Include the header file that defines INPUT and HIGH

class Simple_Button{
  protected:
    int m_pin;                                        // The digital pin the button is connected to.
    int m_debounce_ms;                                // The number of milliseconds for debouncing
    unsigned long m_last_event_time;                  // Timestamp of the last event
    boolean m_current_state;                          // The current state of the button
    void (*callback_function)();                      // the function to be called on a button press event.
    char m_serial_handle;
    void send_serial();

  public:
    Simple_Button();                                                                // The default constructor
    Simple_Button(int pin, int debounce_milliseconds, const char &serial_handle);   // An overloaded constructor 
    bool check_button_pressed();                                                    // Call this to see if the button is being pressed
    void set_callback_func(void (*f)());                                            // Set the callback function  
};
#endif
