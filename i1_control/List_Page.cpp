#include "List_Page.h"

List_Page::List_Page(Menu_Controller *menu_controller, Parameter_Container *parameter_container):Menu_Page(menu_controller, parameter_container){
}

void List_Page::draw(Adafruit_SSD1306 &display){
  char string_buffer[16];                                                       // Buffer for reading strings from program memory.

  display.clearDisplay();                                                       // Clear the display.
  display.setTextColor(WHITE);                                                  // Set text to white.
                                                          
                                                                                // Draw the page title.
  display.setCursor((PADDING),PADDING);                                         // Set the cursor position.
  strcpy_P(string_buffer, (char *)pgm_read_word(&(m_menu_text[0])));            // Copy title string into flash memory; always index 0.
  
  display.println(string_buffer);                                               // Write text to display.
  display.drawLine(0, 14, 128, 14, WHITE);                                      // Underline the title.

  for(int i = 1; i < m_number_of_menu_items; i++){                              // Iterate through the remaining strings in the array.
     
    if(m_menu_controller->get_cursor_position() == i-1){                        // Print the cursor if in text location
      display.setCursor((PADDING),(LINE_HEIGHT * i) + (PADDING));               
      display.println('>');                                                     
    }                                                                           
    
    display.setCursor((PADDING + WHITE_SPACE),(LINE_HEIGHT * i) + (PADDING));   // Print the text.
    strcpy_P(string_buffer, (char *)pgm_read_word(&(m_menu_text[i])));
    display.println(string_buffer);                                             
  }
  display.display();                                                            // Display the new image.                 
}
