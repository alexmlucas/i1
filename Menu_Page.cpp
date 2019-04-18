#include "Menu_Page.h"

Menu_Page::Menu_Page(char const *menu_type, char const *menu_location, Menu_Controller *menu_controller, Parameter_Container *parameter_container){
  /*for(int i = 0; i < sizeof(menu_type); i++){
    m_menu_type[i] = menu_type[i];
  }*/
  
  // Assign class member pointers to incoming memory addresses.
  m_menu_controller = menu_controller;
  m_parameter_container = parameter_container;
}

void Menu_Page::set_text(const char *const *menu_text){
  m_menu_text = menu_text;
}

void Menu_Page::set_location(char const *location){
  /*for(int i = 0; i < sizeof(location); i++){
    m_location[i] = location[i];
  }*/
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
  
  display.println(string_buffer);                                           // Write text to display.
  display.drawLine(0, 14, 128, 14, WHITE);                                  // Underline the title.
 
  for(int i = 1; i < NUMBER_OF_LINES; i++){                                 // Interate through the remaining strings in the array.

    if(m_menu_controller->get_cursor_position() == i-1){                    // Is the cursor in the same position as the text?
      
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

void Menu_Page::set_cursor_disabled(bool cursor_disabled){
  m_cursor_disabled = cursor_disabled;
}

void Menu_Page::set_enter_disabled(bool enter_disabled){
  m_enter_disabled = enter_disabled;
}

void Menu_Page::set_back_disabled(bool back_disabled){
  m_back_disabled = back_disabled;
}
