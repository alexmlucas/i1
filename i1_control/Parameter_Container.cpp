#include "Parameter_Container.h"

Parameter_Container::Parameter_Container(Menu_Controller *menu_controller){
  // Eventually I'll need to load in the saved parameters from the RPi here.
  // *** If I replace this class with a struct, parameters can be loaded in in the setup{} function. ***
  m_menu_controller = menu_controller;
  m_selected_song = 0;
  m_selected_song_char ='w';
  //m_selected_guitar = 0;
  //m_selected_guitar_char ='x';
  m_test_parameter_1.value = 29;
  m_test_parameter_1.character = 'h';
}

void Parameter_Container::set_selected_song(int parameter_value){
  Serial.println(m_selected_song_char);
  m_selected_song = parameter_value;
  m_menu_controller->set_redraw_display_flag(true);
}

void Parameter_Container::set_selected_guitar(int parameter_value){
  Serial.println(m_selected_guitar_char);
  m_selected_guitar = parameter_value;
  m_menu_controller->set_redraw_display_flag(true);
}

void Parameter_Container::set_parameter(Parameter *parameter, int value){
  parameter->value = value;
  Serial.println(parameter->character);
  // We won't always need to redraw the display. Perhaps parameters should have a value which determines whether or
  // not the display needs to be redrawn.
  //m_menu_controller->set_redraw_display_flag(true);
}
