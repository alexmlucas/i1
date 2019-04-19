#include "Menu_Controller.h"

Menu_Controller::Menu_Controller(int cursor_min_value, int cursor_max_value){
    m_cursor_position = 0;
    m_cursor_min_value = cursor_min_value;
    m_cursor_max_value = cursor_max_value;
    m_current_menu_location = '0';
    set_redraw_display_flag(true);
}

void Menu_Controller::increment_cursor_position(){
  m_cursor_position++;
  set_redraw_display_flag(true);
}

void Menu_Controller::decrement_cursor_position(){
  m_cursor_position--;
  set_redraw_display_flag(true);
}

int Menu_Controller::get_cursor_position(){
  return m_cursor_position;
}

int Menu_Controller::get_cursor_max_value(){
  return m_cursor_max_value;
}

int Menu_Controller::get_cursor_min_value(){
  return m_cursor_min_value;
}

bool Menu_Controller::get_redraw_display_flag(){
  return m_redraw_display_flag;
}

void Menu_Controller::set_redraw_display_flag(bool redraw_display_flag){
  m_redraw_display_flag = redraw_display_flag;
}

void Menu_Controller::set_currently_selected_menu(void *currently_selected_menu){
  m_currently_selected_menu = currently_selected_menu;                              // Update the currently selected menu.
  set_redraw_display_flag(true);                                                    // Set the flag to redraw the display.
}

void* Menu_Controller::get_currently_selected_menu(){
  return m_currently_selected_menu;
}
