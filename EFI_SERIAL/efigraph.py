import glob
import pickle
import matplotlib.pyplot as plt
import numpy as np
import math

def main():

  # Choose and open file
  files = glob.glob('./tests/*')
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
  mpavg = list(sensors['MAP_AVG'])
  rpm = list(sensors['RPM'])
  tps = list(sensors['TPS'])
  revs = list(sensors['totalRevs'])
  mpt = list(sensors['MAPTrough'])
  mptlen = list(np.ones(len(mpt)))
  dmap = list(sensors['dMAP'])
  gmap = list(sensors['gMAP'])
  dmapPos = [a > 0 for a in dmap]
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
  plt.plot(ms, mpavg, color='purple')
  plt.plot(ms, gmap, color='pink')
  #plt.plot(ms, np.convolve(mp, [20/28,5/28,2/28,1/28], 'same'), color='purple')
  ax2 = plt.twinx()
  ax2.scatter(ms, drevs, color='green', label='dRevs')
  ax2.scatter(ms, sensors['INJECTED'], color='orange', label='Injected')
  ax2.scatter(mpt, mptlen, color='red', label='MAP Trough')
  #ax2.scatter(ms, dmapPos, color='red', label='dMAP is Positive')
  #for i in range(len(mpt)):
   # ax2.axvline(x=mpt[i])
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
