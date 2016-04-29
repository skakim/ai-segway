import matplotlib.pyplot as plt

with open("20160428180251.txt") as f:
    data = f.read()

data = data.split('\n')

x = [i for i in range(len(data))]
y = [row for row in data]

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("'Simulated Annealing'")
ax1.set_xlabel('Iterations')
ax1.set_ylabel('Performance')
#ax1.axvline(10,0,20000)
#ax1.axvline(110,0,20000)
#ax1.axvline(210,0,20000)
#ax1.axvline(310,0,20000)
#ax1.axvline(410,0,20000)
#ax1.axvline(510,0,20000)
#ax1.axvline(610,0,20000)

ax1.plot(x,y, c='r', marker='o', ls='')

leg = ax1.legend()

plt.show()
fig.savefig('SimulatedAnnealing.png')
