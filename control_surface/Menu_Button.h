#ifndef MENU_BUTTON
#define MENU_BUTTON
#include "Arduino.h"
#include "Menu_Controller.h"
#include "Simple_Button.h"

class Menu_Button: public Simple_Button{
  protected:
    void (*callback_function)(Menu_Controller*);      // the function to be called on a button press event.
    Menu_Controller *m_menu_controller;               // Pointer to the menu_controller

  public:
    Menu_Button(int debounce_milliseconds, Menu_Controller *menu_controller);
    Menu_Button(int pin, int debounce_milliseconds, Menu_Controller *menu_controller);    
    bool check_button_pressed();                                                           // Call this to see if the button is being pressed
    void set_callback_func(void (*f)(Menu_Controller*));                                   // Set the callback function, expects a pointer to a function which expects a pointer to a Menu_Controller
};
#endif
