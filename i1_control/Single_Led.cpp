#include "Single_Led.h"                           

Single_Led::Single_Led(int pin){
  m_pin = pin;
  m_on_value = 255;
  m_flash_flag = false;
  m_currently_on = false;
  m_flash_rate_ms = 250;
  pinMode(m_pin, OUTPUT);
  analogWrite(m_pin, m_currently_on);
}

void Single_Led::set_on(bool _state){
  switch(_state){
    case _OFF:
      analogWrite(m_pin, 0);
      m_currently_on = false;
      break;
    case _ON:
      Serial.println("switching on");
      analogWrite(m_pin, m_on_value);
      m_currently_on = true;
      break;
  }
}

void Single_Led::set_flashing(bool _state){
  m_flash_flag = _state;
  m_currently_on = false;
  analogWrite(m_pin, 0);
}

void Single_Led::update_flashing(){
  if(m_flash_flag == true){
    if((millis() - m_last_flash_time) > m_flash_rate_ms){
      m_currently_on = !m_currently_on;

      if(m_currently_on == true){
        analogWrite(m_pin, m_on_value);
      } else {
        analogWrite(m_pin, 0);
      }

      m_last_flash_time = millis();
    }
  }
}
