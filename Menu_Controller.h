#ifndef MENU_CONTROLLER
#define MENU_CONTROLLER
#include "Arduino.h"

class Menu_Controller{
  protected:
    int m_cursor_position;
    int m_cursor_max_value;
    int m_cursor_min_value;
    char m_current_menu_location;
    bool m_redraw_display_flag;
    
  public:
    void *m_currently_selected_menu;            // Generic pointer for pointing to currently selected menu.
    Menu_Controller(int cursor_min_value, int cursor_max_value);
    void increment_cursor_position();
    void decrement_cursor_position();
    int get_cursor_position();
    int get_cursor_max_value();
    int get_cursor_min_value();
    bool get_redraw_display_flag();
    void set_redraw_display_flag(bool redraw_display_flag);
    void move_menu_location_forwards();
    void move_menu_location_backwards();
    char get_current_menu_page();
    void set_currently_selected_menu(void *currently_selected_menu);
    void* get_currently_selected_menu();
};
#endif
