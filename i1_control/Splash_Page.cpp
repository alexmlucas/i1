#include "Splash_Page.h"

Splash_Page::Splash_Page(const char *const *menu_text, Menu_Controller *menu_controller, Parameter_Container *parameter_container, int *number_of_menu_items):Menu_Page(menu_text, menu_controller, parameter_container, number_of_menu_items){
  m_enter_enabled = false;
  m_back_enabled = false;
  m_encoder_enabled = false;
}

void Splash_Page::draw(Adafruit_SSD1306 &display){
  char string_buffer[16];                                                       // Buffer for reading strings from program memory.

  display.clearDisplay();                                                       // Clear the display.
  display.setTextColor(WHITE);                                                  // Set text to white.

  for(int i = 0; i < *m_number_of_menu_items; i++){                              // Iterate through the remaining strings in the array.
     
    display.setCursor((PADDING),(LINE_HEIGHT * i) + PADDING);                   // Print the text.
    strcpy_P(string_buffer, (char *)pgm_read_word(&(m_menu_text[i])));
    display.println(string_buffer);                                             
  }
  display.display();                                                            // Display the new image.                 
}
