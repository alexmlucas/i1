#include "Parameter_Container.h"

Parameter_Container::Parameter_Container(){
  m_selected_song = 3;
}

int Parameter_Container::get_selected_song(){
  return m_selected_song;
}
    
void Parameter_Container::set_selected_song(int selected_song){
  m_selected_song = selected_song;
}
