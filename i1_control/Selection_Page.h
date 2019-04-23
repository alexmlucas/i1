#ifndef SELECTION_PAGE
#define SELECTION_PAGE
#include "Arduino.h"                            // Include the header file that defines INPUT and HIGH
#include "Menu_Page.h"                          // Include the parent class

class Selection_Page: public Menu_Page{
  public:
    Selection_Page(Menu_Controller *menu_controller, Parameter_Container *parameter_container);
    void on_enter();
    virtual void draw(Adafruit_SSD1306 &display);
};
#endif
