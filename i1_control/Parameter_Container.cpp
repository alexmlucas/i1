#include "Parameter_Container.h"

Parameter_Container::Parameter_Container(){
  // Eventually I'll need to load in the saved parameters from the RPi here.
  // *** If I replace this class with a struct, parameters can be loaded in in the setup{} funciton. ***
  m_selected_song = 0;
  m_selected_guitar = 0;
}
