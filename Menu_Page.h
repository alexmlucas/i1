#ifndef MENU_PAGE
#define MENU_PAGE
#include "Arduino.h"
#include "Menu_Controller.h"
#include "Parameter_Container.h"
#include <Adafruit_SSD1306.h>

const int PADDING PROGMEM = 3;
const int LINE_HEIGHT PROGMEM = 15;
const int NUMBER_OF_LINES PROGMEM = 4;
const int WHITE_SPACE PROGMEM = 16;

class Menu_Page{
  protected:
    bool m_cursor_disabled;
    bool m_enter_disabled;
    bool m_back_disabled;
    char m_menu_type[];
    char const *m_location;
    char m_string_buffer[30];                                         // Buffer used when copying strings from Program Memory to RAM.
    const char *const *m_menu_text;                                   // A pointer to an array of constant pointers to constant chars.
    Menu_Controller *m_menu_controller;                               // Pointer to the menu_controller
    Parameter_Container *m_parameter_container;                       // Pointer to the parameter_container.
    Menu_Page *m_sub_menus[3];                                         // Array of pointers to sub menus.
    
  public:
    Menu_Page(char const *menu_type, char const *menu_location, Menu_Controller *menu_controller, Parameter_Container *parameter_container);
    void set_location(char const *location);
    void set_cursor_disabled(bool cursor_disabled);
    void set_enter_disabled(bool cursor_disabled);
    void set_back_disabled(bool cursor_disabled);
    void set_text(const char *const *menu_text);
    void set_sub_menus(Menu_Page *sub_menus[3]);
    void draw(Adafruit_SSD1306 &display);
    void on_enter();
};
#endif
