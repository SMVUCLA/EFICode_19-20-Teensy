import glob
import pickle
import matplotlib.pyplot as plt

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
  drevs = [0, 0] + drevs[:]
  print(len(drevs))
  print(len(ms))

  for i in range(0,500):
    rpm[rpm.index(max(rpm))] = 0
  
  #
  # Injection Time vs Micros
  #
  plt.figure(2)
  plt.plot(ms, mp)
  ax2 = plt.twinx()
  ax2.scatter(ms, sensors['INJECTED'], color='orange')
  ax2.scatter(ms, drevs, color='green')
  for i in range(len(drevs)):
    if drevs[i] > 0:
      ax2.axvline(x=ms[i])
  plt.tight_layout()
  plt.title('MAP vs Micros')


  plt.figure(4)
  plt.plot(sensors['micros'],sensors['MAP_AVG'])
  plt.grid()
  plt.title('dMicros vs len(dMicros)')
  
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
