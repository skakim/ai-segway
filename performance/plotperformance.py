import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

with open("20160428180251.txt") as f:
    data = f.read()

data = data.split('\n')

x = [i for i in range(0,len(data))]
y = [row for row in data]

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("'Simulated Annealing'")
ax1.set_xlabel('Iterations')
ax1.set_ylabel('Performance')

#ax1.axvline(9,0,20000)
#for i in range(109,709,100):
#    ax1.axvline(i,0,20000)

ax1.plot(x,y, c='r', marker='o', ls='')

leg = ax1.legend()

#plt.xlim(0, 709)
plt.ylim(0, 20000)

intx = [int(i) for i in x]
inty = [int(i) for i in y]

learning = np.polyfit(intx,inty,3)
p = np.poly1d(learning)
ax1.plot(x,p(x),c='b',lw=5)

plt.show()
fig.savefig('SimulatedAnnealingCurve.png')
