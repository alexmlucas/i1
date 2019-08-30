#ifndef PARAMETER_CONTAINER
#define PARAMETER_CONTAINER
#include "Arduino.h"
#include "Parameter.h"

class Parameter_Container{
  public:
    Parameter m_master_level;
    Parameter m_song;
    Parameter m_guitar;
    Parameter m_guitar_level;
    Parameter m_backing_level;
    Parameter m_red_scale;
    Parameter m_green_scale;
    Parameter m_blue_scale;
    Parameter m_red_root;
    Parameter m_green_root;
    Parameter m_blue_root;
    Parameter m_zone;
    Parameter m_reconnect;
    Parameter m_power;
    Parameter m_play;
    Parameter m_song_loaded;
    
    Parameter_Container();
    void set_parameter(Parameter *parameter, int value);
    void set_and_send_parameter(Parameter *parameter, int value);
};
#endif
