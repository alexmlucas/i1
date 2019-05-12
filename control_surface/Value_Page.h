#ifndef VALUE_PAGE
#define VALUE_PAGE
#include "Arduino.h"                            // Include the header file that defines INPUT and HIGH
#include "Menu_Page.h"                          // Include the parent class

class Value_Page: public Menu_Page{
  protected:
    const char *const *m_parameter_text;                                   // A pointer to an array of constant pointers to constant chars.
    int m_parameter_max_value;
  public:
    Value_Page(Menu_Controller *menu_controller, Parameter_Container *parameter_container);
    void on_encoder(uint8_t *pin_value);
    void draw(Adafruit_SSD1306 &display);
    void set_and_send_parameter_text(const char *const *parameter_text, int number_of_parameter_items);
};
#endif
