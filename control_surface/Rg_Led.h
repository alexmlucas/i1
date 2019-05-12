#ifndef RG_LED
#define RG_LED
#include "Arduino.h"
#include "Single_Led.h"

#define _OFF 0

class Rg_Led: public Single_Led{ 
     int m_pins[2];
     int m_colour[2];
  public:
    Rg_Led();
    void set_pinout(int pins[2]);
    void set_colour(int colour[2]);
    void set_flashing(bool _state);
    void update_flashing();
};
#endif
