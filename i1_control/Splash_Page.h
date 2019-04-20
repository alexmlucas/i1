#ifndef SPLASH_PAGE
#define SPLASH_PAGE
#include "Arduino.h"                            // Include the header file that defines INPUT and HIGH
#include "Menu_Page.h"                          // Include the parent class

class Splash_Page: public Menu_Page{  
  public:
    Splash_Page(const char *const *menu_text, Menu_Controller *menu_controller, Parameter_Container *parameter_container, int *number_of_menu_items);
    void draw(Adafruit_SSD1306 &display);
};
#endif
