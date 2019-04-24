#ifndef RGB_LED
#define RGB_LED
#include "Arduino.h"

#define _OFF 0

class Rgb_Led{ 
     int m_pins[3];
     int m_colour[3];
  public:
    Rgb_Led(int pins[3]);
    void set_colour(int colour[3]);
};
#endif
