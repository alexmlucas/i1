#ifndef MENU_PAGE
#define MENU_PAGE
#include "Arduino.h"
#include "Menu_Controller.h"
#include "Parameter_Container.h"
#include <Adafruit_SSD1306.h>

const int PADDING PROGMEM = 3;
const int LINE_HEIGHT PROGMEM = 15;
const int WHITE_SPACE PROGMEM = 16;

class Menu_Page{
  protected:
    char m_string_buffer[30];                                         // Buffer used when copying strings from Program Memory to RAM.
    const char *const *m_menu_text;                                   // A pointer to an array of constant pointers to constant chars.
    Menu_Controller *m_menu_controller;                               // Pointer to the menu_controller.
    Parameter_Container *m_parameter_container;                       // Pointer to the parameter_container.
    Menu_Page *m_sub_menus[3];                                        // Array of pointers to sub menus.
    Menu_Page *m_previous_menu;                                       // Pointer to previous menu.
    int m_number_of_menu_items;
    
  public:
    bool m_enter_enabled;
    bool m_back_enabled;
    bool m_encoder_enabled;
    Menu_Page(const char *const *menu_text, Menu_Controller *menu_controller, Parameter_Container *parameter_container);
    void set_sub_menus(Menu_Page *sub_menus[3]);
    void set_previous_menu(Menu_Page *previous_menu);
    virtual void draw(Adafruit_SSD1306 &display);
    virtual void on_enter();
    virtual void on_back();
    virtual void on_encoder(uint8_t *pin_value);
};
#endif
