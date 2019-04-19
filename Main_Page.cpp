#include "Main_Page.h"

Main_Page::Main_Page(const char *const *menu_text, Menu_Controller *menu_controller, Parameter_Container *parameter_container):Menu_Page(menu_text, menu_controller, parameter_container){
  m_menu_text = menu_text;                                                      // Set the menu text.
  m_menu_controller = menu_controller;                                          // Assign class member pointers to incoming memory addresses.
  m_parameter_container = parameter_container;
}

void Main_Page::draw(Adafruit_SSD1306 &display){
  char string_buffer[16];                                                       // Buffer for reading strings from program memory.
  char param_buffer_1[] = " ";                                                  // First buffer for parameter value
  char param_buffer_2[0];                                                       // Second buffer for parameter value

  sprintf(param_buffer_2, "%d", (m_parameter_container->get_selected_song()+1));    // Get the selected song value, convert to 'char. Add 1 to remove zero index for displaying.
  strcat(param_buffer_1, param_buffer_2);                                           // Concatenate the two parameter buffers
  
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

bool Main_Page::on_back(){
  return false;
}
