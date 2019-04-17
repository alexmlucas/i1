#ifndef MENU_PAGE
#define MENU_PAGE
#include "Arduino.h"
#include <Adafruit_SSD1306.h>

const int PADDING PROGMEM = 2;

class Menu_Page{
  protected:
    char m_items[4][8];
    bool m_cursor_disabled;
    bool m_enter_disabled;
    bool m_back_disabled;
    char m_menu_type[];
    char m_location[];
    char *const m_menu_txt[];
    // Buffer used when copying strings from Program Memory to RAM.
    char m_string_buffer[30];
    // a pointer to type const char.
    const char *m_string;
    
  public:
    Menu_Page(char menu_type[]);
    void set_location(char location[]);
    void set_cursor_disabled(bool cursor_disabled);
    void set_enter_disabled(bool cursor_disabled);
    void set_back_disabled(bool cursor_disabled);
    void set_text(const char *menu_txt);
    void draw(Adafruit_SSD1306 &display);
};
#endif
