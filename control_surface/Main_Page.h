#ifndef MAIN_PAGE
#define MAIN_PAGE
#include "Arduino.h"                            // Include the header file that defines INPUT and HIGH
#include "Menu_Page.h"                          // Include the parent class
#include "Parameter.h"                          
                      


class Main_Page: public Menu_Page{ 
  public:
    Main_Page(Menu_Controller *menu_controller, Parameter_Container *parameter_container);
    void draw(Adafruit_SSD1306 &display);
};
#endif
