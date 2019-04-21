#include "Value_Page.h"

Value_Page::Value_Page(Menu_Controller *menu_controller, Parameter_Container *parameter_container, int *target_parameter):Menu_Page(menu_controller, parameter_container){
  m_target_parameter = target_parameter;
  m_enter_enabled = false;
}

void Value_Page::set_parameter_text(const char *const *parameter_text, int number_of_parameter_items){
  m_parameter_text = parameter_text; 
  m_number_of_parameter_items = number_of_parameter_items;
  m_parameter_max_value = m_number_of_parameter_items - 1;
}

void Value_Page::draw(Adafruit_SSD1306 &display){
  char string_buffer[16];                                                       // Buffer for reading strings from program memory.
  int selected_value = *m_target_parameter;                                     // The selected item equals the value at the address pointed to by m_target_parameter.          
  
  display.clearDisplay();                                                       // Clear the display.
  display.setTextColor(WHITE);                                                  // Set the text to white.
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

void Value_Page::on_encoder(uint8_t *pin_value){
  
  if(*pin_value == LOW){                                                        // If true, a clockwise rotation has occured.
    Serial.println("pin low");
    Serial.println(m_parameter_max_value);

    if(*m_target_parameter < m_parameter_max_value){                            // If the max parameter value has not yet been reached...
      Serial.println("increment");
      (*m_target_parameter)++;                                                  // ...increment the target parameter.  
      m_menu_controller->set_redraw_display_flag(true);                         // Redraw the display.
    }
  } else if (*m_target_parameter > 0){                                          // If the code reaches this point, an anti-clockwise rotation has occured...
      Serial.println("pin high");
      (*m_target_parameter)--;                                                  // ...check to see if the target parameterr is above the minimum allowed and decrement if so.
      m_menu_controller->set_redraw_display_flag(true);                         // Redraw the display.
  }  
}
