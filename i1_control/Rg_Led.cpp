#include "Rg_Led.h";

Rg_Led::Rg_Led(){
  int m_currently_on[3] = {false, false};
}

void Rg_Led::set_pinout(int pins[3]){
  for(int i = 0; i < 2; i++){
    m_pins[i] = pins[i];                  // Set the pin values
    m_colour[i] = 0;                      // Set the LED colours, default to off.
    pinMode(m_pins[i], OUTPUT);           // Set the pin to OUTPUT
    analogWrite(m_pins[i], m_colour[i]);  // Write the colour values to the pins.
  }
}

void Rg_Led::set_colour(int colour[2]){
  for(int i = 0; i < 2; i++){
    m_colour[i] = colour[i];              // Set the colour values
    analogWrite(m_pins[i], m_colour[i]);  // Write the colour values to the pins.
  }
}

void Rg_Led::set_flashing(bool _state){
  m_flash_flag = _state;
  m_currently_on = false;
  
  for(int i = 0; i < 2; i++){
    analogWrite(m_pins[i], 0);
  }
}

void Rg_Led::update_flashing(){
  for(int i = 0; i < 2; i++){
    
    if(m_flash_flag == true){
      if((millis() - m_last_flash_time) > m_flash_rate_ms){
        m_currently_on = !m_currently_on;

        if(m_currently_on == true){
          for(int i = 0; i < 2; i++){
            analogWrite(m_pins[i], m_colour[i]);
          }
          
        } else {
          for(int i = 0; i < 2; i++){
            analogWrite(m_pins[i], 0);
          }
        }
        m_last_flash_time = millis();
      }
    }
  } 
}
