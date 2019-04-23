#ifndef PARAMETER_CONTAINER
#define PARAMETER_CONTAINER
#include "Arduino.h"
#include "Parameter.h"

class Parameter_Container{
  public:
    Parameter m_song;
    Parameter m_guitar;
    Parameter m_guitar_level;
    Parameter m_backing_level;
    Parameter m_master_level;
    Parameter m_red_scale;
    Parameter m_green_scale;
    Parameter m_blue_scale;
    Parameter m_red_root;
    Parameter m_green_root;
    Parameter m_blue_root;
    Parameter m_selected_zone;
    
    Parameter_Container();
    void set_parameter(Parameter *parameter, int value);
    void get_parameter_value(Parameter *parameter, int value);
};
#endif
