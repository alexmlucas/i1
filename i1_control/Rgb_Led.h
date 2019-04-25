#ifndef RGB_LED
#define RGB_LED
#include "Arduino.h"
#include "Single_Led.h"

#define _OFF 0

class Rgb_Led: public Single_Led{ 
     int m_pins[3];
     int m_colour[3];
  public:
    Rgb_Led();
    void set_pinout(int pins[3]);
    void set_colour(int colour[3]);
    void set_flashing(bool _state);
    void update_flashing();
};
#endif
