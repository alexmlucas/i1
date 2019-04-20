#include "Menu_Page.h"

Menu_Page::Menu_Page(const char *const *menu_text, Menu_Controller *menu_controller, Parameter_Container *parameter_container){
  m_menu_text = menu_text;                                                      // Set the menu text.
  m_menu_controller = menu_controller;                                          // Assign class member pointers to incoming memory addresses.
  m_parameter_container = parameter_container;
  m_enter_enabled = true;
  m_back_enabled = true;
  m_encoder_enabled = true;
}

void Menu_Page::set_sub_menus(Menu_Page *sub_menus[]){
  for(int i = 0; i < 3; i++){
    m_sub_menus[i] = sub_menus[i];
  }
  /*Serial.print("The class array is pointing to this address: ");
  Serial.println((int)&*m_sub_menus[0]);*/
}

void Menu_Page::set_previous_menu(Menu_Page *previous_menu){
  m_previous_menu = previous_menu;
}

void Menu_Page::draw(Adafruit_SSD1306 &display){
  char string_buffer[16];                                                       // Buffer for reading strings from program memory.
  char param_buffer_1[] = " ";                                                  // First buffer for parameter value
  char param_buffer_2[0];                                                       // Second buffer for parameter value

  sprintf(param_buffer_2, "%d", m_parameter_container->get_selected_song());    // Get the selected song value, convert to 'char'
  strcat(param_buffer_1, param_buffer_2);                                       // Concatenate the two parameter buffers
  
  display.clearDisplay();                                                       // Clear the display.
                                                          
                                                                                // Draw the page title.
  display.setCursor((PADDING),PADDING);                                         // Set the cursor position.
  strcpy_P(string_buffer, (char *)pgm_read_word(&(m_menu_text[0])));            // Copy title string into flash memory; always index 0.
  
  strcat(string_buffer, param_buffer_1);                                        // Concatenate the menu text string with the parameter buffer.
  
  display.println(string_buffer);                                               // Write text to display.
  display.drawLine(0, 14, 128, 14, WHITE);                                      // Underline the title.
 
  for(int i = 1; i < NUMBER_OF_LINES; i++){                                     // Iterate through the remaining strings in the array.

    if(m_menu_controller->get_cursor_position() == i-1){                        // Is the cursor in the same position as the text?
      
      display.setCursor((PADDING),(LINE_HEIGHT * i) + (PADDING));               // Calculate and set the cursor position.
      display.println('>');                                                     // Print the cursor.
      display.setCursor((PADDING + WHITE_SPACE),(LINE_HEIGHT * i) + (PADDING)); // Calculate and set the text position.
      strcpy_P(string_buffer, (char *)pgm_read_word(&(m_menu_text[i])));        // Copy text string into flash memory.
      display.println(string_buffer);                                           // Write the text to the display.
    } else {
                                                                                // The cursor is not the same position as the text...
      display.setCursor((PADDING + WHITE_SPACE),(LINE_HEIGHT * i) + (PADDING)); // ...so just write the text string.
      strcpy_P(string_buffer, (char *)pgm_read_word(&(m_menu_text[i])));
      display.println(string_buffer);
    }
  }
  display.display();                                                            // Display the new image.                 
}

bool Menu_Page::on_enter(){
  int cursor_position = m_menu_controller->get_cursor_position();               // Get the current cursor position.
  m_menu_controller->set_currently_selected_menu(m_sub_menus[cursor_position]); // Update the currently selected menu.
  return true;
}

bool Menu_Page::on_back(){
  m_menu_controller->set_currently_selected_menu(m_previous_menu);              // Update the currently selected menu to previous.
  return true;
}

void Menu_Page::on_encoder(uint8_t *pin_value){
  if(*pin_value == LOW){                                                                            // If true, a clockwise rotation has occured.
    if(m_menu_controller->get_cursor_position() < m_menu_controller->get_cursor_max_value()){       // If the max cursor value has not yet been reached...
      m_menu_controller->increment_cursor_position();                                               // ...increment the cursor position.               
    }
  } else if (m_menu_controller->get_cursor_position() > m_menu_controller->get_cursor_min_value()){ // If the code reaches this point, an anti-clockwise rotation has occured...
    m_menu_controller->decrement_cursor_position();                                                 // ...check to see if the cursor position is above the minimum allowed and decrement if so.
  }  
}
