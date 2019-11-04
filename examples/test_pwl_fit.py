from scipy import optimize
import matplotlib.pyplot as plt
from gekko import GEKKO
import numpy as np

m = GEKKO()
m.options.SOLVER = 3
m.options.IMODE = 2

xzd = np.linspace(1,5,100)
yzd = np.sin(xzd)

xz = m.Param(value=xzd)
yz = m.CV(value=yzd)
yz.FSTATUS = 1

xp_val = np.array([1, 2, 3, 3.5,   4, 5])
yp_val = np.array([1, 0, 2, 2.5, 2.8, 3])
xp = [m.FV(value=xp_val[i],lb=xp_val[0],ub=xp_val[-1]) for i in range(6)]
yp = [m.FV(value=yp_val[i]) for i in range(6)]
for i in range(6):
    xp[i].STATUS = 0
    yp[i].STATUS = 1
for i in range(5):
    m.Equation(xp[i+1]>=xp[i]+0.05)

x = [m.Var(lb=xp[i],ub=xp[i+1]) for i in range(5)]
x[0].lower = -1e20
x[-1].upper = 1e20

# Variables
slk_u = [m.Var(value=1,lb=0) for i in range(4)]
slk_l = [m.Var(value=1,lb=0) for i in range(4)]

# Intermediates
slope = []
for i in range(5):
    slope.append(m.Intermediate((yp[i+1]-yp[i]) / (xp[i+1]-xp[i])))

y = []
for i in range(5):
    y.append(m.Intermediate((x[i]-xp[i])*slope[i]))

for i in range(4):
    m.Obj(1000*(slk_u[i] + slk_l[i]))

m.Equation(xz == x[0]   + slk_u[0])
for i in range(3):
    m.Equation(xz == x[i+1] + slk_u[i+1] - slk_l[i])
m.Equation(xz == x[4] - slk_l[3])

m.Equation(yz == yp[0] + y[0] + y[1] + y[2] + y[3] + y[4])

m.solve()
#y_val = yz.value
#print(y_val)

import matplotlib.pyplot as plt
plt.plot(xp,yp,'rx-',label='PWL function')
plt.plot(xzd,yzd,'b.',label='Data')
plt.show()
