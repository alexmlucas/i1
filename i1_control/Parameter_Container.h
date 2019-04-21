#ifndef PARAMETER_CONTAINER
#define PARAMETER_CONTAINER
#include "Arduino.h"

class Parameter_Container{
  public:
    int m_selected_song;
    int m_selected_guitar;
    int m_guitar_level;
    int m_backing_level;
    int m_master_level;
    int m_red_scale;
    int m_green_scale;
    int m_blue_scale;
    int m_red_root;
    int m_green_root;
    int m_blue_root;
    int m_selected_zone;

    // each parameter needs an associated char.
    // could each parameter be a pointer to a struct which has two members,
    // a parameter value and a char. In doing this we could have a generic set method.
    Parameter_Container();
    // Include set methods here from each parameter which also sends a serial message.
};
#endif
