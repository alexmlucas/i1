#include "Rgb_Led.h"

Rgb_Led::Rgb_Led(){
  int m_currently_on[3] = {false, false, false};
}

void Rgb_Led::set_pinout(int pins[3]){
  for(int i = 0; i < 3; i++){
    m_pins[i] = pins[i];                  // Set the pin values.
    pinMode(m_pins[i], OUTPUT);           // Set the pin to OUTPUT
    analogWrite(m_pins[i], 0);            // Default state of off.
  }
}

void Rgb_Led::set_colour(int *colour){
  Serial.println((int)colour);
  m_colour = colour;
  
  for(int i = 0; i < 3; i++){
    Serial.print(*(m_colour+i));
    analogWrite(m_pins[i], *(m_colour+i));  // Write the colour values to the pins.
  }
}

void Rgb_Led::set_flashing(bool _state){
  m_flash_flag = _state;
  m_currently_on = false;
  
  for(int i = 0; i < 3; i++){
    analogWrite(m_pins[i], 0);
  }
}

void Rgb_Led::update_flashing(){
  for(int i = 0; i < 3; i++){
    
    if(m_flash_flag == true){
      if((millis() - m_last_flash_time) > m_flash_rate_ms){
        m_currently_on = !m_currently_on;

        if(m_currently_on == true){
          for(int i = 0; i < 3; i++){
            analogWrite(m_pins[i], m_colour[i]);
          }
          
        } else {
          for(int i = 0; i < 3; i++){
            analogWrite(m_pins[i], 0);
          }
        }
        m_last_flash_time = millis();
      }
    }
  } 
}
