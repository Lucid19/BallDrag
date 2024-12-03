import matplotlib.pyplot as plt
import math

# code parameters
# absolute ball speed initial
vin =27

# ball, positive aimed above horizontal, negative aimed below horizontal
bearing=45

# wind, positive forward on x, negative backward on x
vw=0

#height from which it is thrown
height=1.5

tmax=5
h=0.01

vxi=vin*math.cos((bearing/180)*math.pi)
vyi=vin*math.sin((bearing/180)*math.pi)

# projectile type
m=0.15
r=0.03

# physical constants
C=0.47
d=1.0
A=math.pi*(r**2)
g=9.8
k=(0.5*C*d*A)/m

def rk4(h, f, vin):
    v = vin
    t=0
    vValues= [vin]
    while t < tmax:
        t+=h
        k1=h*f(v)
        k2=h*f(v+k1/2)
        k3=h*f(v+k2/2)
        k4=h*f(v+k3)
        v+=(k1+2*k2+2*k3+k4)/6
        vValues.append(v)
    return vValues

def dvx_dt(vx):
    if(vx<vw and vw >= 0):
        return k*((vx-vw)**2)
    else:
        return -k*((vx-vw)**2)

def dvy_dt(vy):
    if vy > 0:
        return -g -k*(vy**2)
    else:
        return -g +k*(vy**2)

def x(h):
    xValues=rk4(h, dvx_dt, vxi)
    x=[0]
    for i in range(len(xValues)):
        x.append(xValues[i]*h+x[i])
    return x
def y(h):
    yValues=rk4(h, dvy_dt, vyi)
    y=[height]
    for i in range(len(yValues)):
        y.append(yValues[i]*h+y[i])
    return y

def xreg(h):
    x=[0]
    t=0
    while t < tmax:
        t+=h
        x.append(vxi*t)
    return x

def yreg(h):
    y=[height]
    t=0
    while t < tmax:
        t+=h
        y.append(vyi*t - 0.5*g*(t**2)+height)
    return y

plt.plot(x(h), y(h))
plt.plot(xreg(h), yreg(h))
plt.show()