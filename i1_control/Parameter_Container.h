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
    Parameter_Container();
    int get_selected_song();
    void set_selected_song(int selected_song);
};
#endif
