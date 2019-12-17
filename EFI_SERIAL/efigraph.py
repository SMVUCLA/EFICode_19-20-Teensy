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
  plt.figure(1)
  plt.hist2d(sensors['MAP_INDEX'],sensors['RPM_INDEX'])
  plt.colorbar()
  plt.grid()
  plt.title('RPM_INDEX vs MAP_INDEX')

  ms = sensors['micros']
  ipt = sensors['injectorPulseTime']
  
  #for i in range(0,10):
  #  ix = ms.index(max(ms))
  #  del ms[ix]
  #  del ipt[ix]
  
  plt.figure(2)
  plt.scatter(ms, ipt)
  plt.grid()
  plt.title('Injection Time vs Micros')
 
  plt.figure(3)
  plt.scatter(range(len(ms)), ms)
  plt.grid()
  plt.title('Micros vs len(micros)')
  
  dms = [b - a for b, a in zip(ms[1:-1], ms[0:-2])]
  plt.figure(4)
  plt.scatter(range(len(dms)),dms)
  plt.grid()
  plt.title('dMicros vs len(dMicros)')
  plt.show()

if __name__ == "__main__":
  main()
