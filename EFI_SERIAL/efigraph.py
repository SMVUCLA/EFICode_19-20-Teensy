import pickle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

#style.use('dark_background')

with open('f19w9/330091142(opened throttle, pulsed)', 'rb') as df:
    sensors = pickle.load(df)

#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)
#ax1 = fig.add_subplot(1,1,1)
  

def main():
  plt.figure(1);
  plt.hist2d(sensors['MAP_INDEX'],sensors['RPM_INDEX'])
  plt.colorbar()
  plt.grid()
  

  ms = sensors['micros']
  ipt = sensors['injectorPulseTime']

  for i in range(0,10):
    ix = ms.index(max(ms))
    del ms[ix]
    del ipt[ix]
  
  plt.figure(2);
  plt.scatter(ms, ipt)
  plt.grid()

  plt.show()

if __name__ == "__main__":
  main()
