#include "Controller.h"

#include "Constants.h"
#include "TimerThree.h"
//#include "EEPROM.h"

Controller *c;

void setup() {
  // Construct Controller object.
  c = new Controller();

  // Update all sensor values to current values.
  c->updateRPM();
  c->readSensors();

  // Attach rpm detector to revolution counter interrupt.
  // For some reason, the internal interrupt flags can end up defaulting
  // to a triggered state before they are attached. This causes them
  // to trigger once right when they are attached. Our current workaround
  // is to attach the interrupt to a dummy function first that triggers
  // if the interrupt is already set. Then, it is safe to attach the normal interrupt.
  attachInterrupt(digitalPinToInterrupt(HES_Pin), dummy, FALLING);
  detachInterrupt(digitalPinToInterrupt(HES_Pin));
  attachInterrupt(digitalPinToInterrupt(HES_Pin), countRev, FALLING);

  // Initialize pulseOff timer.
  Timer3.initialize(1000000);

  // Attach the interrupt for INJ pulse modulation.
  // For some reason, the internal interrupt flags can end up defaulting
  // to a triggered state before they are attached. This causes them
  // to trigger once right when they are attached. Our current workaround
  // is to attach the interrupt to a dummy function first that triggers
  // if the interrupt is already set. Then, it is safe to attach the normal interrupt.
  Timer3.attachInterrupt(dummy);
  Timer3.detachInterrupt();
  Timer3.attachInterrupt(handle_pulseTimerTimeout);

  // FOR CHANGING PARAMETERS WITH BUTTON PRESSES
  //attachInterrupt(digitalPinToInterrupt(2), lowerStartupMod, FALLING);
  //attachInterrupt(digitalPinToInterrupt(3), raiseStartupMod, FALLING);
  
  // Immediately stop the timer.
  Timer3.stop();

  pinMode(LED_1, OUTPUT);  
  digitalWrite(LED_1, HIGH);
}

void loop() {
  //Update RPM if needed.
  c->updateRPM();

  // Update Controller with most recent sensor values.
  c->readSensors();

  // Look up injection time on each loop cycle
  c->lookupPulseTime();

  // Adjust injectorBasePulseTime[][] Values by using feedback loop with O2 sensor.
  c->AFRFeedback();
  c->idleRPMFeedback();
 
  // Checks the status of the engine. e.g., detects whether the engine is on or off.
  c->checkEngineState();

  // Attempt to send sensor data to the DAQ system. Will only occur if the
  // currentlySendingData flag is set to true. This flag is set by sending 
  // the ID 1 signal to the controller.
  c->trySendingData();

  // Check for commands from Serial port.
  c->getCommand();
}

void countRev() {
  c->countRevolution();
}

void handle_pulseTimerTimeout() {
  if(digitalRead(LED_1) == 0){
    digitalWrite(LED_1, HIGH);
  }else{
    digitalWrite(LED_1, LOW);
  }
  c->pulseOff();
}

void lowerStartupMod() {
  c->lowerStartupModifier();
  Serial.println("lower");
}

void raiseStartupMod() {
  c->raiseStartupModifier();
  Serial.println("raise");
}

void dummy() {}
