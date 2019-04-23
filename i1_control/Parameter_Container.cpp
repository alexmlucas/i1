#include "Parameter_Container.h"

Parameter_Container::Parameter_Container(){
  // Eventually I'll need to load in the saved parameters from the RPi here.

  m_song.value = 0;
  m_song.character = 'a';

  m_guitar.value = 0;
  m_guitar.character = 'b';
  
  m_guitar_level.value = 0;
  m_guitar_level.character = 'c';
  
  m_backing_level.value = 0;
  m_backing_level.character = 'd';
  
  m_master_level.value = 0;
  m_master_level.character = 'e';
  
  m_red_scale.value = 0;
  m_red_scale.character = 'f';
  
  m_green_scale.value = 0;
  m_green_scale.character = 'g';
  
  m_blue_scale.value = 0;
  m_blue_scale.character = 'h';
  
  m_red_root.value = 0;
  m_red_root.character = 'i';
  
  m_green_root.value = 0;
  m_green_root.character = 'j';
  
  m_blue_root.value = 0;
  m_blue_root.character = 'k';
  
  m_selected_zone.value = 0;
  m_selected_zone.character = 'l';
}

void Parameter_Container::set_parameter(Parameter *parameter, int value){
  parameter->value = value;
  Serial.println(parameter->character);
  // We won't always need to redraw the display. Perhaps parameters should have a value which determines whether or
  // not the display needs to be redrawn.
  
  //m_menu_controller->set_redraw_display_flag(true);
}
