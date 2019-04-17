#include "Menu_Page.h"

Menu_Page::Menu_Page(char menu_type[]){
  for(int i; i < sizeof(menu_type); i++){
    m_menu_type[i] = menu_type[i];
  }
}

void Menu_Page::set_text(const char *menu_txt){
  m_string = menu_txt;
}


void Menu_Page::set_location(char location[]){
  for(int i; i < sizeof(location); i++){
    m_location[i] = location[i];
  }
}

void Menu_Page::draw(Adafruit_SSD1306 &display){
  display.clearDisplay();
  display.setCursor(PADDING,0 + PADDING);
  display.println(F("Song 1"));
  display.setCursor(PADDING, 16 + PADDING);
  display.println(F("> Guitar"));
  display.setCursor(PADDING + 13, 32 + PADDING);
  display.println(F("Zone"));
  display.setCursor(PADDING + 13, 48 + PADDING);
  display.println(F("Mix"));

  display.drawLine(0, 14, 128, 14, WHITE);
  display.display();
  Serial.println("hey you!");
  Serial.println(int(m_string));
  Serial.println(char(pgm_read_byte_near(m_string)));
  Serial.println(char(pgm_read_byte_near(m_string+1)));
  Serial.println("yes you!");

  char myChar;

  for(byte k = 0; k < strlen_P(m_string); k++){
    myChar = pgm_read_byte_near(m_string + k);
    Serial.print(myChar);
  }

  Serial.println();

  
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
