#ifndef PARAMETER_CONTAINER
#define PARAMETER_CONTAINER
#include "Arduino.h"
#include "Menu_Controller.h"
#include "Parameter.h"

class Parameter_Container{
  public:
    Menu_Controller *m_menu_controller;
    int m_selected_song;
    char m_selected_song_char;
    
    int m_selected_guitar;
    char m_selected_guitar_char;

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

    Parameter m_test_parameter_1;
    Parameter m_test_parameter_2;
    
    // each parameter needs an associated char.
    // could each parameter be a pointer to a struct which has two members,
    // a parameter value and a char. In doing this we could have a generic set method.
    Parameter_Container(Menu_Controller *menu_controller);
    // Include set methods here from each parameter which also sends a serial message.
    void set_selected_song(int parameter_value);
    void set_selected_guitar(int parameter_value);
    void set_parameter(Parameter *parameter, int value);
};
#endif
