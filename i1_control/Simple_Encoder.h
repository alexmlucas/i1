#ifndef SIMPLE_ENCODER
#define SIMPLE_ENCODER
#include "Arduino.h"                                                  // Include the header file that defines INPUT and HIGH.
#include "Menu_Controller.h"

class Simple_Encoder{
  private:
    int m_pin_A;                                                      // Encoder pin A.
    int m_encoder_A_last;                                             // Last value of encoder pin A.
    int m_pin_B;                                                      // Encoder pin B.
    int m_debounce_ms;                                                // Number of milliseconds for debouncing.
    unsigned long m_last_event_time;                                  // Timestamp.
    int m_encoder_position;                                           // Current position of the encoder.
    int m_encoder_max;                                                // Sets the maximum value.
    int m_encoder_min;                                                // Sets the minimum value.
    Menu_Controller *m_menu_controller;                               // Pointer to the menu_controller; needed for encoder position.

  public:
    Simple_Encoder();                                                                                       // Constructor
    void initialise(int pin_A, int pin_B, int debounce_milliseconds, Menu_Controller *menu_controller);
    int get_position();                                                                                     // Get current position of encoder
    int track_position();                                                                                   // Call this in main loop() to track the position
};
#endif
