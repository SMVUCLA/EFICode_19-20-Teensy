#ifndef CONST_H
#define CONST_H

//Auxiliary Functions
void countRev();
void handle_pulseTimerTimeout();
void enableINJ();
void disableINJ();
void dummy();
void lowerStartupMod();

// Define all the pin numbers
const int HES_Pin = 19;
const int TPS_Pin = 13; // updated (analog)
const int ECT_Pin = 19; // updated (analog)
const int MAP_Pin = 16; // updated (analog)
const int IAT_Pin = 18; // updated (analog)
const int INJ_Pin = 31; // updated (digital)
const int FP_Pin = 17;  // updated (analog)
//const int FRS_Pin = 6; // don't have
const int SP1 = 7;
const int OIN1_Pin = SP1;
const int OIN2_Pin = 4;
const int SP2 = 8;
const int SP3 = 39;
const int SP4 = 37;

const double Vs_5 = 5.00; //Volts
const double Vs_3v3 = 3.30; //Volts

// Multiple by this number to convert analog readings to voltages from Op amps
const double adcRef = 3.30; //Volts
const double opampVoltageDivider = 1000.0 / (1000 + 470);
const double adcToOpampVin = adcRef / (1023 * opampVoltageDivider);
const double voltageConversion = 5.0 / 1023;

// Constants for calculating estimated injection times.
const double engineDisplacement = 49.4E-6;    //meters^3
const double airSpecificGasConstant = 286.9;   //Joules / (kilograms * Kelvin)
const double injectorFuelRate   = 2.13333E-3;    //kilograms per second
const double injectionConstant  = 
              engineDisplacement / (airSpecificGasConstant * injectorFuelRate);
              // meters^2 / (kilograms * microseconds * Kelvin) 
const int openTime              = 350;          // Estimated amount of time for injector to open in microseconds.

// Controls the total number of revolutions 
const int numRevsForStart = 25;

// Number of magnets the hall effect sensor must detect for one full revolution
const int numMagnets = 2;

// Define the range of values for RPM and Manifold Air Pressure
const int maxRPM = 8000;    // In revolutions / minute
const int minRPM = 120;     // In revolutions / minute
const unsigned long maxMAP = 120000;     // In Pa
const unsigned long minMAP = 20000;      // In Pa

// Define the number of rows and number of columns for the AFR Table.
const int numTableRows = 11;
const int maxTableRowIndex = numTableRows - 1;
const int numTableCols = 16;
const int maxTableColIndex = numTableCols - 1;

// Define the range of values that an AFR table value can take.
const int MIN_AFR = 8;
const int MAX_AFR = 18;

// Define the range of values that the Intake air temperature can take.
const int MIN_IAT = 200;  // In Kelvin
const int MAX_IAT = 500;  // In Kelvin

// Define the range of values that the Throttle Position value can take.
const int MIN_TPS = 0;
const int MAX_TPS = 1;

// Define the BAUD_RATE to communicate with.
const unsigned long BAUD_RATE = 250000; // In bits per second;

// Engine is considered off if it has RPM less than the minimum RPM.
const int SHUTOFF_RPM = minRPM;

// Minimum time that must pass per revolution before the engine can be considered off.
// Given in microseconds.
// (60 sec / min) * (10^6 microsecond / sec) * (SHUTOFF_RPM min / revolution) = (SHUTOFF_DELAY microseconds / revolution)
const unsigned long int SHUTOFF_DELAY = 6E7 / SHUTOFF_RPM ; 

#endif
