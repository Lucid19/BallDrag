import matplotlib.pyplot as plt
import math

# code parameters
# absolute ball speed initial
vin =27

# ball, positive aimed above horizontal, negative aimed below horizontal
bearingZ=45

# ball, positive aimed at the left, negative aimed at the right
bearingY=70

# wind, positive to the left negative to the right
windBearing=0

# wind, positive forward on x, negative backward on x
vw=20

#height from which it is thrown
height=1.5

vxi=vin*math.cos((bearingZ/180)*math.pi)
vzi=vin*math.sin((bearingZ/180)*math.pi)
vyi=vin*math.sin((bearingY/180)*math.pi)

vywind= vw*math.sin((windBearing/180)*math.pi)
vxwind= vw*math.cos((windBearing/180)*math.pi)
h=0.01
tmax=20

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

def dvy_dt(vy):
    if(vy<vywind and vywind >= 0):
        return k*((vy-vywind)**2)
    else:
        return -k*((vy-vywind)**2)
    
def dvx_dt(vx):
    if(vx<vxwind and vxwind >= 0):
        return k*((vx-vxwind)**2)
    else:
        return -k*((vx-vxwind)**2)

def dvz_dt(vz):
    if vz > 0:
        return -g -k*(vz**2)
    else:
        return -g +k*(vz**2)

def x(h, max):
    xValues=rk4(h, dvx_dt, vxi)
    x=[0]
    i=0
    while i < max:
        x.append(xValues[i]*h+x[i])
        i+=1
    return x

def y(h, max):
    yValues=rk4(h, dvy_dt, vyi)
    y=[0]
    i=0
    while i < max:
        y.append(yValues[i]*h+y[i])
        i+=1
    return y

def z(h):
    zValues=rk4(h, dvz_dt, vzi)
    z=[height]
    max=0
    for i in range(len(zValues)):
        z.append(zValues[i]*h+z[i])
        if z[i+1] <= 0:
            max=i+1
            break
    return [z, max]

def simulateDragTraj(h):
    zRes = z(h)

    xVals = x(h, zRes[1])
    yVals = y(h, zRes[1])

    return [xVals, yVals, zRes[0]]

def xreg(h, max):
    x=[0]
    t=0
    while t < max:
        t+=h
        x.append(vxi*t)
    return x

def yreg(h, max):
    y=[0]
    t=0
    while t < max:
        t+=h
        y.append(vyi*t)
    return y

def zreg(h):
    z=[height]
    t=0
    i=0
    while t < tmax:
        t+=h
        z.append(vzi*t - 0.5*g*(t**2)+height)
        if(z[int(t/h)]<=0):
            break
    return [z, t]

def simulateNormTraj(h):
    zRes = zreg(h)

    xVals = xreg(h, zRes[1])
    yVals = yreg(h, zRes[1])
    
    return [xVals, yVals, zRes[0]]


data1 = simulateDragTraj(h)
data2= simulateNormTraj(h)

ax= plt.axes(projection="3d")

ax.plot(data1[0], data1[1], data1[2])
ax.plot(data2[0], data2[1], data2[2])
ax.set_xlabel("X (m)")
ax.set_ylabel("Y (m)")
ax.set_zlabel("Z (m)")
plt.show()