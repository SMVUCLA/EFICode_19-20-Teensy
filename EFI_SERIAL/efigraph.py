import pickle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

#style.use('dark_background')

with open('330091142(opened throttle, pulsed)', 'rb') as df:
    sensors = pickle.load(df)

#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)
#ax1 = fig.add_subplot(1,1,1)
  

def main():
  
  #plt.scatter(sensors[time], sensors[o2])
  
  #get rid of really high data time values
  i = 0
  while i < len(sensors['micros']):
    if sensors['micros'][i] > 3.0e8 or sensors['micros'][i] < 2.9e8:
      for k in range(0,len(sensors.keys())):
        del sensors[list(sensors.keys())[k]][i]
        continue;
    i+=  1
  
  # #get rid of when MAP is off
  # i = 0
  # while i < len(sensors['MAP']):
    # if sensors['MAP'] == 0:
      # for k in range(0,len(sensors.keys())):
        # del sensors[list(sensors.keys())[k]][i]
        # continue
    # i += 1
      
  plt.plot(sensors['micros'], sensors['MAP'])
  #plt.scatter(sensors['micros'], sensors['injectorPulseTime'])
  plt.grid()
  plt.show()

if __name__ == "__main__":
  main()
