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
#define HES_Pin A14//36 // (GP3) updated (digital) 
#define TPS_Pin A13 // updated (analog)
#define ECT_Pin A19 // updated (analog)
#define MAP_Pin A15//A16 // updated (analog)
#define IAT_Pin A18 // updated (analog)
#define INJ_Pin 31 // updated (digital)
#define FP_Pin A17  // updated (analog)
//const int FRS_Pin = 6; // don't have
#define SP1 7
#define OIN1_Pin 36//A14
#define OIN2_Pin A16// A15
#define SP2 8
#define SP3 39
#define SP4 37

#define LED_1 5

const double Vs_5 = 5.00; //Volts
const double Vs_3v3 = 3.30; //Volts


// Multiple by this number to convert analog readings to voltages from Op amps
const double adcRef = Vs_3v3; //Volts
const double maxADC = 1023;
const double voltageConversion = adcRef / maxADC;
const double opampVoltageDivider = 1000.0 / (1000 + 470);
const double adcToOpampVin = adcRef / (maxADC * opampVoltageDivider);

// Constants for calculating estimated injection times.
const double engineDisplacement = 49.4E-6;    //meters^3
const double airSpecificGasConstant = 286.9;   //Joules / (kilograms * Kelvin) (from Ideal Gas / Molecular Mass of Air
const double injectorFuelRate   = 10E-3;    //kilograms per second
const double injectionConstant  = 
              engineDisplacement / (airSpecificGasConstant * injectorFuelRate);
              // meters^2 / (kilograms * microseconds * Kelvin) 
const int openTime = 1000;          // Estimated amount of time for injector to open in microseconds.

// Controls the total number of revolutions 
const int numRevsForStart = 25;

// Number of magnets the hall effect sensor must detect for one full revolution
const int numMagnets = 1;

// Define the range of values that an AFR table value can take.
const int MIN_AFR = 8;
const int MAX_AFR = 18;

// Define the range of values that the Intake air temperature can take.
const int MIN_IAT = 200;  // In Kelvin
const int MAX_IAT = 500;  // In Kelvin
const int MAX_ALLOWABLE_ECT = 400; // CHANGE********************************************************************

// Define the range of values that the Throttle Position value can take.
const int MIN_TPS = 0;
const int MAX_TPS = 1;

// Define the BAUD_RATE to communicate with.
const unsigned long BAUD_RATE = 921600; // In bits per second;
const int DATA_RATE_PERIOD = 5000; // send back data every 5 ms

// Define the range of values for RPM and Manifold Air Pressure
const int maxRPM = 8000;    // In revolutions / minute
const int minRPM = 120;     // In revolutions / minute
const unsigned long maxMAP = 120000;     // In Pa
const unsigned long minMAP = 20000;      // In Pa

const unsigned long minDelayPerRev = (1 / (8000 * (1/60))) * (1E6); // in units of microseconds
const unsigned int revsPerCalc = 5;

// Define the number of rows and number of columns for the AFR Table.
static const int numTableRows = 11;
static const int numTableCols = 10;


// Engine is considered off if it has RPM less than the minimum RPM.
const int SHUTOFF_RPM = 120;

// Minimum time that must pass per revolution before the engine can be considered off.
// Given in microseconds.
// (60 sec / min) * (10^6 microsecond / sec) * (SHUTOFF_RPM min / revolution) = (SHUTOFF_DELAY microseconds / revolution)
const unsigned long int SHUTOFF_DELAY = 1E6; // below 60 RPM is shutoff

#endif
