#include "Rgb_Led.h";

Rgb_Led::Rgb_Led(int pins[3]){
  for(int i = 0; i < 3; i++){
    m_pins[i] = pins[i];                  // Set the pin values
    m_colour[i] = 0;                     // Set the LED colours, default to off.
    pinMode(m_pins[i], OUTPUT);           // Set the pin to OUTPUT
    analogWrite(m_pins[i], m_colour[i]); // Write the colour values to the pins.
  }
}

void Rgb_Led::set_colour(int colour[3]){
  for(int i = 0; i < 3; i++){
    m_colour[i] = colour[i];              // Set the colour values
    analogWrite(m_pins[i], m_colour[i]); // Write the colour values to the pins.
  }
}
