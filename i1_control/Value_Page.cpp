#include "Value_Page.h"

Value_Page::Value_Page(const char *const *menu_text, const char *const *parameter_text, Menu_Controller *menu_controller, Parameter_Container *parameter_container, int *target_parameter):Menu_Page(menu_text, menu_controller, parameter_container){
  m_menu_text = menu_text;                                                      // Set the menu text.
  m_menu_controller = menu_controller;                                          // Assign class member pointers to incoming memory addresses.
  m_parameter_container = parameter_container;
  m_target_parameter = target_parameter;
  m_parameter_text = parameter_text;
}

void Value_Page::draw(Adafruit_SSD1306 &display){
  char string_buffer[16];                                                       // Buffer for reading strings from program memory.
  int selected_value = *m_target_parameter;                                     // The selected item equals the value at the address pointed to by m_target_parameter.          
  
  display.clearDisplay();                                                       // Clear the display.
  display.setTextColor(WHITE);                            
                                                                                // Draw the page title.
  display.setCursor((PADDING),PADDING);                                         // Set the cursor position.
  strcpy_P(string_buffer, (char *)pgm_read_word(&(m_menu_text[0])));            // Copy title string into flash memory; always index 0.
  
  display.println(string_buffer);                                               // Write text to display.
  display.drawLine(0, 14, 128, 14, WHITE);                                      // Underline the title.

  display.fillRect(0, LINE_HEIGHT + 1, 90, 12, WHITE);
  display.setCursor(PADDING, LINE_HEIGHT + PADDING);
  display.setTextColor(BLACK);
  strcpy_P(string_buffer, (char *)pgm_read_word(&(m_parameter_text[selected_value])));
  display.println(string_buffer);
  
  display.display();                                                            // Display the new image.                 
}
bool Value_Page::on_enter(){
  return false;
}
