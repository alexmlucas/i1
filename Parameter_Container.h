#ifndef PARAMETER_CONTAINER
#define PARAMETER_CONTAINER
#include "Arduino.h"

class Parameter_Container{
  protected:  
    int m_selected_song;
  public:
    Parameter_Container();
    int get_selected_song();
    void set_selected_song(int selected_song);
};
#endif
