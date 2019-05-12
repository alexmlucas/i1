#include "Menu_Page.h"

Menu_Page::Menu_Page(Menu_Controller *menu_controller, Parameter_Container *parameter_container){                                                     
  m_menu_controller = menu_controller;
  m_parameter_container = parameter_container;
  m_enter_enabled = true;
  m_back_enabled = true;
  m_encoder_enabled = true;
}

void Menu_Page::set_and_send_parameter_struct(Parameter *parameter_struct){
  m_parameter_struct = parameter_struct; 
}

void Menu_Page::set_menu_text(const char *const *menu_text, int number_of_menu_items){
  m_menu_text = menu_text; 
  m_number_of_menu_items = number_of_menu_items;
}

void Menu_Page::set_sub_menus(Menu_Page *sub_menus[]){
  for(int i = 0; i < m_number_of_menu_items; i++){
    m_sub_menus[i] = sub_menus[i];
  }
}

void Menu_Page::set_previous_menu(Menu_Page *previous_menu){
  m_previous_menu = previous_menu;
}

void Menu_Page::draw(Adafruit_SSD1306 &display){
  display.clearDisplay();                                                       // Clear the display.
  display.display();                                                            // Display the new image.                 
}

void Menu_Page::on_enter(){
  int cursor_position = m_menu_controller->get_cursor_position();               // Get the current cursor position.
  m_menu_controller->set_currently_selected_menu(m_sub_menus[cursor_position]); // Update the currently selected menu.
}

void Menu_Page::on_back(){
  m_menu_controller->set_currently_selected_menu(m_previous_menu);              // Update the currently selected menu to previous.
}

void Menu_Page::on_encoder(uint8_t *pin_value){  
  if(*pin_value == LOW){                                                          // If true, a clockwise rotation has occured.
    if(m_menu_controller->get_cursor_position() < (m_number_of_menu_items - 2)){  // If the max cursor value has not yet been reached...
      m_menu_controller->increment_cursor_position();                             // ...increment the cursor position.               
    }
  } else if (m_menu_controller->get_cursor_position() > 0){                       // If the code reaches this point, an anti-clockwise rotation has occured...
    m_menu_controller->decrement_cursor_position();                               // ...check to see if the cursor position is above the minimum allowed and decrement if so.
  }  
}
