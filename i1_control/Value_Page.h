#ifndef VALUE_PAGE
#define VALUE_PAGE
#include "Arduino.h"                            // Include the header file that defines INPUT and HIGH
#include "Menu_Page.h"                          // Include the parent class

class Value_Page: public Menu_Page{
  protected:
    const char *const *m_parameter_text;                                   // A pointer to an array of constant pointers to constant chars.
    int *m_target_parameter;  
  public:
    Value_Page(const char *const *menu_text, const char *const *parameter_text, Menu_Controller *menu_controller, Parameter_Container *parameter_container, int *target_parameter);
    bool on_enter();
    virtual void draw(Adafruit_SSD1306 &display);
};
#endif
