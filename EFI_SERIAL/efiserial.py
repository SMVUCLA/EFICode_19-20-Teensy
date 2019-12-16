import os
import serial
from config_loader import Config
import time
import atexit
import pickle

clear = lambda: os.system('cls')

config = 'config.ini'

configContents = "[GEN]\nCOM = 1\nBAUD = 9600\nFILENAMEDATE = n\nFOLDER = default"

sensors = {k: [] for k in 
  ['micros',
   'totalRevs',
   'ECT',
   'IAT',
   'MAP',
   'MAP_AVG',
   'TPS',
   'AFR',
   'RPM',
   'injectorPulseTime',
   'lastPulse',
   'MAP_INDEX',
   'RPM_INDEX',
   'STARTUP_MOD',
   'STARTING_BOOL',
   'INJECTED']}

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
  dataPath = Config.gen('FOLDER')
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
  dataPath = dataPath + '/' +  dataFile

  # open serial port
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

  # collect and log data
  global sensors
  
  numMismatch = 0
  maxMismatch = 5

  allKeys = list(sensors.keys())
  buf = bytearray()
  while True:
    try:

      try:
        buf = buf + ser.read(max(1, ser.in_waiting))
        i = buf.find(b'\n')
        if i >= 0:
            line = buf[:i+1]
            buf = buf[i+1:]
        else:
            continue
      except Exception as e:
        clear()
        print('error')
        continue

      if line == '':
        print('empty buffer')
        continue

      vals = line.split(b':')
      if len(vals) != len(allKeys):
        numMismatch += 1
        if numMismatch >= maxMismatch:
          numMismatch = 0
          print('mismatch in sensor number')
          input('press enter to continue')
          continue
        else:
          continue;
      numMismatch = 0 # if we get here, no consecutive mismatch
      clear()
      output = ''
      for k in range(len(allKeys)):
        sensors[allKeys[k]].append(float(vals[k]))
      for k in sensors:
        output = output + k + ": " + str(float(vals[allKeys.index(k)])) + '\n'
      output = output + 'saving to: ' + dataPath + '\n'
      output = output + 'len of TPS: ' + str(len(sensors['TPS'])) + '\n'
      output = output + 'ctrl-c to save and exit'
      print(output)
    except KeyboardInterrupt:
      with open(dataPath, 'wb') as df:
        pickle.dump(sensors, df) # save file
      exit()
  
  
# end main

def leave():
  input("press enter to exit")
  exit()

if __name__ == '__main__':
  main()
