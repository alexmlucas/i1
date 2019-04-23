#ifndef PARAMETER_CONTAINER
#define PARAMETER_CONTAINER
#include "Arduino.h"

class Parameter_Container{
  public:
    int m_selected_song;
    int m_selected_guitar;
    Parameter_Container();
    int get_selected_song();
    void set_selected_song(int selected_song);
};
#endif
