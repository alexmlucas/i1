#ifndef MAIN_PAGE
#define MAIN_PAGE
#include "Arduino.h"                            // Include the header file that defines INPUT and HIGH
#include "Menu_Page.h"                          // Include the parent class

class Main_Page: public Menu_Page{  
  public:
    Main_Page(const char *const *menu_text, Menu_Controller *menu_controller, Parameter_Container *parameter_container);
    bool on_back();
    void draw(Adafruit_SSD1306 &display);
};
#endif