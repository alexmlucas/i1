const int NUM_READINGS = 10;
// constants for last state of pressure sensor
const int NO_ACTIVITY = 0;
const int DECREMENT = 1;
const int INCREMENT = 2;

int pressureSensorPreviousState = 0; // to track the state of the pressure sensor
int pressureSensorCurrentState = 0; // current state of the pressure sensor
int chordSelector = 1; // the currently selected chord
int chordSelectorPreviousState = 1;
int chordChangeFlag = 0; // has the user requested the chord change?
int readings[NUM_READINGS];  // the readings from the analog input
int readIndex = 0;          // the index of the current reading
int total = 0;              // the running total
int average = 0;            // the average
int ambientReading = 0;     // ambient pressure

int pressureSensorInputPin = A0;
int switchInputPin = 4;

int switchPreviousState = 0; // previous state of the switch
int switchCurrentState = 0; // current state of the switch

unsigned long lastDebounceTime = 0; // the last time the switch value changed
unsigned long debounceDelay = 50; // debounce time

// ledPins
int blueLedPin = 3;
int greenLedPin = 5;
int redLedPin = 6;

void setup() {
  Serial.begin(115200);
  // initialise all readings to 0
  for(int thisReading = 0; thisReading < NUM_READINGS; thisReading++){
    readings[thisReading] = 0;
  }

  // initialise switch pin
  pinMode(switchInputPin, INPUT);
  // initialise pressure sensor pin
  pinMode(pressureSensorInputPin, INPUT);
  // initialise LED pins
  pinMode(blueLedPin, OUTPUT);
  pinMode(greenLedPin, OUTPUT);
  pinMode(redLedPin, OUTPUT);

  updateLed(0);

  delay(100);
}

void loop() {
  // subtract the last reading:
  total = total - readings[readIndex];
  // read from the sensor
  readings[readIndex] = analogRead(pressureSensorInputPin);
  // add the reading to the total:
  total = total + readings[readIndex];
  // advance to the next position in the array:
  readIndex = readIndex + 1;

  // if we're at the end of the array...
  if (readIndex >= NUM_READINGS){
    // ...wrap around to the beginning:
    readIndex = 0;
  }

  // calculate the average:
  average = total / NUM_READINGS;
  delay(1);

  pressureSensorCurrentState = pressureSensorDetector(average);

  if(pressureSensorCurrentState == 1 && pressureSensorPreviousState == NO_ACTIVITY){
    // sip detected
    decrementChordSelector();
    pressureSensorPreviousState = 1;
  }

  if(pressureSensorCurrentState == 2 && pressureSensorPreviousState == NO_ACTIVITY){
    // puff detected
    incrementChordSelector();
    pressureSensorPreviousState = 2;
  }

  if(pressureSensorCurrentState == 0 && pressureSensorPreviousState != NO_ACTIVITY){
    pressureSensorPreviousState = 0;
  }

  // lets process the switch now...
  int switchReading = digitalRead(switchInputPin);

  // if the switch changed, due to noise or pressing
  if(switchReading != switchPreviousState){
    lastDebounceTime = millis();
  }

  if((millis() - lastDebounceTime) > debounceDelay){
    //Serial.println(switchCurrentState);
    // whatever the reading is at, its been there for longer than the debounce
    // delay, so take it as the actual current state

    // if the button state has changed
    if(switchReading != switchCurrentState){
      switchCurrentState = switchReading;

      if(switchCurrentState == HIGH){
        // increment the chord selector
        incrementChordSelector();
      }
    }
  }

  switchPreviousState = switchReading;

  // check for serial data request
  checkForSerialDataRequest();
}

int pressureSensorDetector(int valueFromSensor){
  if(valueFromSensor < 20){
    // sip detected
      return 1;
  } else if(valueFromSensor > 50){
    // puff detected
    return 2;
  } else if (valueFromSensor > 25 && valueFromSensor < 45){
    //no activity
    return 0;
  }
}

// increase chordSelector by 1
void incrementChordSelector(){
  if(chordSelector < 3){
    chordSelector++;
  } else{
    // wrap around when a value of 3 is detected
    chordSelector = 1;
  }
}

// decrease chordSelector by 1
void decrementChordSelector(){
  if(chordSelector > 1){
    chordSelector--;
  } else{
    // wrap around when a value of 1 is detected
    chordSelector = 3;
  }
}

// update the LEDs
void updateLed(int selectedChord){
  switch(selectedChord){
    case 0:
    analogWrite(redLedPin, 0);
    analogWrite(greenLedPin, 0);
    analogWrite(blueLedPin, 0);
    break;
    case 1:
    analogWrite(redLedPin, 128);
    analogWrite(greenLedPin, 0);
    analogWrite(blueLedPin, 0);
    break;
    case 2:
    analogWrite(redLedPin, 0);
    analogWrite(greenLedPin, 128);
    analogWrite(blueLedPin, 0);
    break;
    case 3:
    analogWrite(redLedPin, 0);
    analogWrite(greenLedPin, 0);
    analogWrite(blueLedPin, 128);
    break;
  }
  chordSelectorPreviousState = selectedChord;
}

void checkForSerialDataRequest(){

  int serialCharacter = 0;
  char endMarker = '\n';

  while (Serial.available() > 0){
     serialCharacter = int(Serial.read());

     if (serialCharacter != endMarker){

      if(serialCharacter == 114){


        // Request for IMU data received
        Serial.println(chordSelector);

      } else if (serialCharacter >= 49 && serialCharacter <= 55){

        updateLed(int(serialCharacter - 48));
      }
     }
  }
}
