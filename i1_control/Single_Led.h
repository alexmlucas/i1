#ifndef SINGLE_LED
#define SINGLE_LED
#include "Arduino.h"                            // Include the header file that defines INPUT and HIGH

#define _OFF 0
#define _ON 1

class Single_Led{ 
     int m_pin;
     int m_colour;
     int m_on_value;
  protected:
     bool m_currently_on;
     bool m_flash_flag;
     int m_flash_rate_ms;
     int m_last_flash_time;
  public:
    Single_Led();
    void set_pinout(int pin);
    void set_on(bool _state);
    void set_flashing(bool _state);
    void update_flashing();
};
#endif
