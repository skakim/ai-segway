import matplotlib.pyplot as plt

with open("20160428224143.txt") as f:
    data = f.read()

data = data.split('\n')

x = [i for i in range(0,len(data))]
y = [row for row in data]

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Extended Local Beam Search")
ax1.set_xlabel('Iterations')
ax1.set_ylabel('Performance')

ax1.axvline(9,0,20000)
for i in range(109,4809,100):
    ax1.axvline(i,0,20000)

ax1.plot(x,y, c='r', marker='o', ls='')

leg = ax1.legend()

plt.xlim(0, 4809)
plt.ylim(0, 20000)

plt.show()
fig.savefig('ExtendedLocalBeamSearch.png')
