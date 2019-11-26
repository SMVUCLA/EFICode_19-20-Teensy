import pickle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('dark_background')

time = 'time'
injTime = 'injectionTime'
o2 = 'AFR'

#fig = plt.figure()
#ax1 = fig.add_subplot(1,1,1)
  

def main():
  with open('290165615', 'rb') as df:
    snsrs = pickle.load(df)
  plt.scatter(snsrs[time], snsrs[o2])
  plt.title('time vs o2')
  plt.show()

if __name__ == "__main__":
  main()
