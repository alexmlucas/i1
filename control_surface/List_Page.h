#ifndef LIST_PAGE
#define LIST_PAGE
#include "Arduino.h"                            // Include the header file that defines INPUT and HIGH
#include "Menu_Page.h"                          // Include the parent class

class List_Page: public Menu_Page{  
  public:
    List_Page(Menu_Controller *menu_controller, Parameter_Container *parameter_container);
    void draw(Adafruit_SSD1306 &display);
};
#endif
