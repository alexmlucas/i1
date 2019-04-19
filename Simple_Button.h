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
    void (*callback_function)(Menu_Controller*);      // the function to be called on a button press event.
    char m_serial_handle;
    void send_serial();
    Menu_Controller *m_menu_controller;               // Pointer to the menu_controller

  public:
    Simple_Button();                                                                                                  // The default constructor
    Simple_Button(int pin, int debounce_milliseconds, const char &serial_handle, Menu_Controller *menu_controller);   // An overloaded constructor 
    bool check_button_pressed();                                                                                      // Call this to see if the button is being pressed
    void set_callback_func(void (*f)(Menu_Controller*));                                                              // Set the callback function, expects a pointer to a function which expects a pointer to a Menu_Controller
};
#endif
