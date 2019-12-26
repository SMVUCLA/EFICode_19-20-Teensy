import glob
import pickle
import matplotlib.pyplot as plt
import numpy as np
import math

def main():

  # Choose and open file
  files = glob.glob('./winterbreak/*')
  for n, i in zip(range(0, len(files)), files):
    print('%d %s' %(n,i))
  
  fileN = int(input('which file?\n'))

  with open(files[fileN], 'rb') as df:
    sensors = pickle.load(df)

  # What to display
  #
  # INDEXS USED
  #
  plt.figure(1)
  plt.hist2d(sensors['RPM_INDEX'],sensors['MAP_INDEX'], 20, [[0, 11], [0, 10]])
  plt.colorbar()
  plt.grid()
  plt.gca().invert_yaxis()
  plt.title('MAP_INDEX vs RPM_INDEX')

  ms = list(sensors['micros'])
  ipt = list(sensors['injectorPulseTime'])
  mp = list(sensors['MAP'])
  rpm = list(sensors['RPM'])
  tps = list(sensors['TPS'])
  revs = list(sensors['totalRevs'])
  drevs = [b - a for b, a in zip(revs[1:-1], revs[0:-2])]
  drevs = [0] + drevs[:] + [0]
  print(len(drevs))
  print(len(ms))
  
  for i in range(len(rpm)):
    if(rpm[i] > 8000):
      rpm[i] = rpm[i - 1] # code basically implements this now

  #
  # Injection Time vs Micros
  #
  plt.figure(2)
  plt.plot(ms, mp)
  ax2 = plt.twinx()
  ax2.scatter(ms, drevs, color='green', label='dRevs')
  ax2.scatter(ms, sensors['INJECTED'], color='orange', label='Injected')
  for i in range(len(drevs)):
    if drevs[i] > 0:
      ax2.axvline(x=ms[i])
  plt.tight_layout()
  plt.legend(loc='upper left')
  plt.title('MAP vs Micros')

  plt.figure(3)
  plt.plot(ms, mp)
  ax2 = plt.twinx()
  ax2.plot(ms, rpm, color='green', label='RPM')
  plt.tight_layout()
  plt.legend(loc='upper left')
  plt.title('MAP vs Micros')

  plt.figure(4)
  plt.plot(ms, mp)
  ax2 = plt.twinx()
  ax2.plot(ms, list(np.convolve(sensors['IAT'], [1/math.sqrt(2 * math.pi), 1/math.sqrt(2 * math.exp(1) * math.pi), 1/math.sqrt(2 * math.exp(4) * math.pi)], 'same')), color='green')
  plt.title('MAP/IAT vs ms')
  
  #
  # dMicros
  #
  #dms = [b - a for b, a in zip(ms[1:-1], ms[0:-2])]
  #plt.figure(4)
  #plt.scatter(range(len(dms)),dms)
  #plt.grid()
  #plt.title('dMicros vs len(dMicros)')
  plt.show()

if __name__ == "__main__":
  main()
