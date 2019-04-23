#include "Parameter_Container.h"

Parameter_Container::Parameter_Container(){
  // Eventually I'll need to load in the saved parameters from the RPi here.
  m_selected_song = 0;
  m_selected_guitar = 1;
}

int Parameter_Container::get_selected_song(){
  return m_selected_song;
}
    
void Parameter_Container::set_selected_song(int selected_song){
  m_selected_song = selected_song;
}
