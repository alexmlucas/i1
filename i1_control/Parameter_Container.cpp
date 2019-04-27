#include "Parameter_Container.h"

Parameter_Container::Parameter_Container(){
  // Eventually I'll need to load in the saved parameters from the RPi here.

  m_master_level.value = 0;
  m_song.value = 0;
  m_guitar.value = 0;
  m_guitar_level.value = 0;
  m_backing_level.value = 0;
  m_red_scale.value = 0;
  m_green_scale.value = 0;
  m_blue_scale.value = 0;
  m_red_root.value = 0;
  m_green_root.value = 0;
  m_blue_root.value = 0;
  m_zone.value = 0;
  m_reconnect.value = 0;
  m_power.value = 0;
  m_play.value = 0;

  m_master_level.character = 'a';
  m_song.character = 'b';
  m_guitar.character = 'c';
  m_guitar_level.character = 'd';
  m_backing_level.character = 'e';
  m_red_scale.character = 'f';
  m_green_scale.character = 'g';
  m_blue_scale.character = 'h';
  m_red_root.character = 'i';
  m_green_root.character = 'j';
  m_blue_root.character = 'k';
  m_zone.character = 'l';
  m_reconnect.character = 'm';
  m_power.character = 'n';
  m_play.character = 'o';
}

void Parameter_Container::set_parameter(Parameter *parameter, int value){
  parameter->value = value;
}

void Parameter_Container::set_and_send_parameter(Parameter *parameter, int value){
  char serial_char[2];
  parameter->value = value;

  // Send the identifying character
  Serial.print(parameter->character);

  // Now, what to do with the parameter value?
  // If the parameter is < 10...
  if(parameter->value < 10){
    // Use serial_char to add a leading 0 to meet the requirement of all serial messages to
    // be three characters in length.
    serial_char[0] = '0';
    serial_char[1] = '0' + parameter->value;    // This statement gives us the char representation of the parameter value

    // Send the message.
    Serial.print(serial_char[0]);
    Serial.println(serial_char[1]);
  } else {
    // Otherwise just send the parameter value.
    Serial.println(parameter->value);
  }
  
  
}
