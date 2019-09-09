/*#include <Adafruit_ATParser.h>
#include <Adafruit_BLEMIDI.h>
#include <Adafruit_BLEBattery.h>
#include <Adafruit_BLEGatt.h>
#include <Adafruit_BLEEddystone.h>*/

#include <Adafruit_BLE.h>
#include <Adafruit_BluefruitLE_UART.h>
#include <Adafruit_BluefruitLE_SPI.h>
#include "Adafruit_BLEGatt.h"
#include "BluefruitConfig.h"

#if SOFTWARE_SERIAL_AVAILABLE
  #include <SoftwareSerial.h>
#endif

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>
  
Adafruit_BNO055 bno = Adafruit_BNO055(55);

#define BNO_SERVICE_UUID128     "36-9B-19-D1-A3-40-49-7E-A8-CE-DA-FA-92-D7-67-93"
#define BNO_YAW_CHAR_UUID128    "94-34-C1-6F-B0-11-45-90-8B-E3-2F-97-D6-3C-C5-49"
#define BNO_MOTOR_CHAR_UUID128  "14-EC-99-94-49-32-4B-DA-99-7A-B3-D0-52-CD-74-21"


// Create the bluefruit object, either software serial...uncomment these lines
/*
SoftwareSerial bluefruitSS = SoftwareSerial(BLUEFRUIT_SWUART_TXD_PIN, BLUEFRUIT_SWUART_RXD_PIN);
Adafruit_BluefruitLE_UART ble(bluefruitSS, BLUEFRUIT_UART_MODE_PIN,
                      BLUEFRUIT_UART_CTS_PIN, BLUEFRUIT_UART_RTS_PIN);
*/

/* ...or hardware serial, which does not need the RTS/CTS pins. Uncomment this line */
// Adafruit_BluefruitLE_UART ble(BLUEFRUIT_HWSERIAL_NAME, BLUEFRUIT_UART_MODE_PIN);

/* ...hardware SPI, using SCK/MOSI/MISO hardware SPI pins and then user selected CS/IRQ/RST */
Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_CS, BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

/* ...software SPI, using SCK/MOSI/MISO user-defined SPI pins and then user selected CS/IRQ/RST */
//Adafruit_BluefruitLE_SPI ble(BLUEFRUIT_SPI_SCK, BLUEFRUIT_SPI_MISO,
//                             BLUEFRUIT_SPI_MOSI, BLUEFRUIT_SPI_CS,
//                             BLUEFRUIT_SPI_IRQ, BLUEFRUIT_SPI_RST);

// A small helper
void error(const __FlashStringHelper*err) {
  Serial.println(err);
  while (1);
}

/* The service information */

int32_t bnoServiceId;
int32_t bnoYawCharId;
int32_t bnoMotorCharId;
/**************************************************************************/
/*!
    @brief  Sets up the HW an the BLE module (this function is called
            automatically on startup)
*/
/**************************************************************************/
const int motorPin = 5;
const int ledPin = 9;
int current_guitar_string = 0;
int last_guitar_string = 0;
int led_flash_time = 2000;
int last_led_flash_time;
int led_on_time = 20;
bool switch_off_led = false;

void setCharValue(int32_t charId, float value, int precision=2){
  // Set the specified characteristic to a floating point value.
  // Construct an AT+GATTCHAR command to send the float value.
  // The command will look like: AT+GATTCHAR=<charId>,<value as array of bytes>
  ble.print(F("AT+GATTCHAR="));
  ble.print(charId, DEC);
  ble.print(F(","));
  ble.println(value, precision);
  
  if (!ble.waitForOK())
  {
    Serial.println(F("Failed to get response!"));
  }
}

void setup(void)
{
  pinMode(motorPin, OUTPUT);
  pinMode(ledPin, OUTPUT);
  digitalWrite(motorPin, LOW);
  analogWrite(ledPin, 5);
  
  // while (!Serial); // required for Flora & Micro
  delay(500);

  boolean success;

  Serial.begin(115200);

  randomSeed(micros());

  /* Initialise the module */
  Serial.print(F("Initialising the Bluefruit LE module: "));

  if ( !ble.begin(VERBOSE_MODE) )
  {
    error(F("Couldn't find Bluefruit, make sure it's in CoMmanD mode & check wiring?"));
  }
  Serial.println( F("OK!") );

  /* Perform a factory reset to make sure everything is in a known state */
  Serial.println(F("Performing a factory reset: "));
  if (! ble.factoryReset() ){
       error(F("Couldn't factory reset"));
  }

  /* Disable command echo from Bluefruit */
  ble.echo(false);

  Serial.println("Requesting Bluefruit info:");
  /* Print Bluefruit information */
  ble.info();

  // this line is particularly require for Flora, but is a good idea
  // anyways for the super long lines ahead!
  // ble.setInterCharWriteDelay(5); // 5 ms

  /* Change the device name to make it easier to find */
  Serial.println(F("Setting device name to 'BNO': "));

  if (! ble.sendCommandCheckOK(F("AT+GAPDEVNAME=BNO")) ) {
    error(F("Could not set device name?"));
  }

  /* Add the Heart Rate Service definition */
  /* Service ID should be 1 */
  Serial.println(F("Adding the BNO Service definition: "));
  success = ble.sendCommandWithIntReply( F("AT+GATTADDSERVICE=UUID128=" BNO_SERVICE_UUID128), &bnoServiceId);
  if (! success) {
    error(F("Could not add BNO service"));
  }

  /* Add the Heart Rate Measurement characteristic */
  /* Chars ID for Measurement should be 1 */
  Serial.println(F("Adding the BNO Yaw characteristic: "));
  success = ble.sendCommandWithIntReply( F("AT+GATTADDCHAR=UUID128=" BNO_YAW_CHAR_UUID128 ", PROPERTIES=0x12, MIN_LEN=2, MAX_LEN=3, VALUE=00=40"), &bnoYawCharId);
    if (! success) {
    error(F("Could not add BNO Yaw characteristic"));
  }

  /* Add the Body Sensor Location characteristic */
  /* Chars ID for Body should be 2 */
  Serial.println(F("Adding the BNO Motor characteristic: "));
  success = ble.sendCommandWithIntReply( F("AT+GATTADDCHAR=UUID128=" BNO_MOTOR_CHAR_UUID128 ", PROPERTIES=0x04, MIN_LEN=1, VALUE=20"), &bnoMotorCharId);
    if (! success) {
    error(F("Could not add BNO Motor characteristic"));
  }

  /* Reset the device for the new service setting changes to take effect */
  Serial.print(F("Performing a SW reset (service changes require a reset): "));
  ble.reset();

  Serial.println();

  /* Initialise the sensor */
  if(!bno.begin())
  {
    /* There was a problem detecting the BNO055 ... check your connections */
    Serial.print("Ooops, no BNO055 detected ... Check your wiring or I2C ADDR!");
    while(1);
  }
  
  delay(1000);
  
  bno.setExtCrystalUse(true);
  setCharValue(bnoMotorCharId, current_guitar_string);

  last_led_flash_time = millis();
}

void loop(void) 
{
  /*int current_time = millis();

  // flash the led
  if(current_time - last_led_flash_time > led_flash_time){
    analogWrite(ledPin, 64);
    last_led_flash_time = current_time;
    switch_off_led = true;
  }

  if(switch_off_led == true){
    if(current_time - last_led_flash_time > led_on_time){
      Serial.println("setting low");
      analogWrite(ledPin, 0);
      switch_off_led = false;
    }
  }*/


  
  /* Get a new sensor event */ 
  sensors_event_t event; 
  bno.getEvent(&event);
  
  // does the yaw position correspond to the position of any of the guitar strings?
  // lots of magic numbers here!!
  if (event.orientation.y <= -3 && event.orientation.y >= -8)
  {
    current_guitar_string = 5;
  } else if (event.orientation.y <= -13 && event.orientation.y >= -18)
  {
    current_guitar_string = 4;
  } else if (event.orientation.y <= -23 && event.orientation.y >= -28)
  {
    current_guitar_string = 3;
  } else if (event.orientation.y <= -33 && event.orientation.y >= -38)
  {
    current_guitar_string = 2;
  } else if (event.orientation.y <= -43 && event.orientation.y >= -48)
  {
    current_guitar_string = 1;
  } else if (event.orientation.y <= -53 && event.orientation.y >= -58)
  {
    current_guitar_string = 0;
  } else 
  {
    current_guitar_string = -1;
  }

  // has the guitar string changed?
  if (current_guitar_string != last_guitar_string)
  {
   // set the yaw characteristic value
    setCharValue(bnoYawCharId, current_guitar_string);
    // trigger the motor
    if (current_guitar_string != -1)
    {
      digitalWrite(motorPin, HIGH);
      delay(50);
      digitalWrite(motorPin, LOW);
    }
    last_guitar_string = current_guitar_string;
  }

  // set the sensor value.
  //setCharValue(bnoYawCharId, event.orientation.y);
  
  // trigger a motor burst if motor characteristic == 1
  /*if (getCharValue(bnoMotorCharId) == 1){
    
    setCharValue(bnoMotorCharId, 0);
  }*/
}

//
