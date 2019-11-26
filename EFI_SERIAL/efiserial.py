import os
import serial
from config_loader import Config
import time
import atexit
import pickle

clear = lambda: os.system('cls')

config = 'config.ini'

configContents = "[GEN]\nCOM = 1\nBAUD = 9600\nFILENAMEDATE = n"

sensors = {k: [] for k in 
  ['micros',
   'totalRevs',
   'ECT',
   'IAT',
   'MAP',
   'MAP_AVG',
   'TPS',
   'AFR',
   'injectorPulseTime',
   'lastPulse',
   'MAP_INDEX',
   'RPM_INDEX',
   'STARTING_BOOL']}

global dataFile
saveOnExit = False

ser = serial.Serial()

def main():

  # if config.ini exists, contine
  #  else create it and exit
  if not os.path.exists(config):
    with open(config, 'w') as cfgFile:
      cfgFile.write(configContents)
    print("created config file")
    leave();
  
  # get settings from file
  try:
    com = 'COM' + Config.gen('COM')
    baudrate = int(Config.gen('BAUD'))
  except:
    print("invalid inputs")
    leave()
  
  # name dataFiles after date and time or user chosen
  global dataFile
  if Config.gen('FILENAMEDATE')[0] == 'y':
    tm = time.localtime()
    dataFile = f'{tm[7]:03}{tm[3]:02}{tm[4]:02}{tm[5]:02}'
  else:
    dataFile = input("file to store data: ")
    while dataFile == "":
      dataFile = input("file to store data: ")
    while os.path.exists(dataFile):
      if input("overwrite existing file? (y for yes): ") == "y":
         break
      else:
         dataFile = input("file to store data: ")
         while dataFile == "":
           dataFile = input("file to store data: ")
  

  # open serial port
  global ser
  ser.baudrate = baudrate
  ser.port = com
  ser.timeout = 2
  print('opening port: ' + com + ' at ' + str(baudrate))
  cnt = 0;
  while not ser.is_open:
    try:
      ser.open()
    except:
      print('opening port: ' + com + ' at ' + str(baudrate) + " try: " + str(cnt))
      cnt += 1
      clear()

  # we can save to a file now
  global saveOnExit
  saveOnExit = True

  # collect and log data
  global sensors

  with open(dataFile, 'wb') as df:
    while True:
      try:
        try:
          line = ser.readline()
        except:
          clear()
          print('error')
          continue
        clear()
        if line == '':
          print('empty buffer')
          continue
        vals = line.split(b':')
        if len(vals) != len(sensors.keys()):
          print('mismatch in sensor number')
          input('press enter to continue')
          continue
        for k in range(0,len(sensors.keys())):
          sensors[list(sensors.keys())[k]].append(float(vals[k]))
        for k in sensors:
          print(k + ": " + str(sensors[k][-1]))
        print('saving to: ' + dataFile)
        print('len of TPS: ' + str(len(sensors['TPS'])))
        print('ctrl-c to save and exit')
      except KeyboardInterrupt:
        pickle.dump(sensors, df) # save file
        exit()
    
    
# end main

def leave():
  input("press enter to exit")
  exit()

if __name__ == '__main__':
  main()
