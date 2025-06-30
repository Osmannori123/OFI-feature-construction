import numpy as np
import numpy.random as random
import matplotlib.pyplot as plt
from scipy import fft
from datetime import datetime
import matplotlib        as mpl
import matplotlib.pyplot as plt
import numpy as np
from numpy import cos, exp, log, pi, sin, sqrt
from random import randrange
import scipy.linalg as linalg
from numpy.fft import rfftn, irfftn, fftfreq
import scipy.fftpack as fft
from numpy.random import default_rng


Np = 32**3  
Nc = 128 
L = 1  
l = L / Nc  
Rsphere = L / 4 
G = 6.67*10-11  
mp = 1  
t0 = 0 
totalMass = Np * mp
tDynamical = np.sqrt((np.pi**2 * Rsphere**3) / (4 * G * totalMass))
def initialConditions(Np):
    rng = default_rng()
    part = np.zeros((Np, 9))

    xr, xtheta, xphi = rng.random((3, Np))  
    r = Rsphere  * xr**(1/3)
    theta = np.arccos(1 - 2 * xtheta)
    phi = 2 * np.pi * xphi

    for i in range(Np):
        x = r[i] * np.sin(theta[i]) * np.cos(phi[i]) + L / 2
        y = r[i] * np.sin(theta[i]) * np.sin(phi[i]) + L / 2
        z = r[i] * np.cos(theta[i]) + L / 2
        part[i, :3] = [x, y, z]  

    return part

def densityF(part):
    densityArray = np.zeros((Nc, Nc, Nc))
    for particle in part:
        x, y, z = particle[:3]
        i = int(x // l)
        j = int(y // l)
        k = int(z // l)
        densityArray[i, j, k] += mp / (l**3)
    return densityArray


def potential(density):
    densityk = rfftn(density)
    wk = omegak(densityk.shape)
    potentialk = densityk * wk
    potential = irfftn(potentialk) * (L / Nc)**2
    return potential

def omegak(shape):
    Nkx, Nky, Nkz = shape
    Nk = Nkx
    wk = np.zeros((Nkx, Nky, Nkz))
    for i in range(Nkx):
        if i <= Nk //2:
            kx = 2*np.pi*i / Nk
        else:
            kx = 2*np.pi*(i-Nk) / Nk
        for j in range(Nky):
            if j <= Nk //2:
                ky = 2*np.pi*j / Nk
            else:
                ky = 2*np.pi*(j-Nk) / Nk
            for k in range(Nkz):
                kz = (2 * np.pi * k) / Nk
                if i == j == k == 0:
                    wk[i, j, k] = 0
                else:
                    wk[i, j, k] = -(4 * np.pi * G) / ((2 * np.sin(kx / 2))**2 + (2 * np.sin(ky / 2))**2 + (2 * np.sin(kz / 2))**2)
    return wk

def force(phi):
    x, y, z = phi.shape
    force = np.zeros((x, y, z, 3))
    delta = L/Nc
    fx = None
    fy = None
    fz = None
    for i in range(x):
        for j in range(y):
           for k in range(z):
               if i == 0:
                   fx = -(phi[i+1, j, k] - phi[i, j, k]) / delta
               elif i == x-1:
                   fx = -(phi[i, j, k] - phi[i-1, j, k]) / delta
               else: 
                   fx =  -(phi[i+1, j, k] - phi[i-1, j, k]) / (2*delta)

               if j == 0:
                   fy = -(phi[i, j+1, k] - phi[i, j, k]) / delta
               elif j == y-1:
                   fy = -(phi[i, j, k] - phi[i, j-1, k]) / delta
               else: 
                   fy =  -(phi[i, j+1, k] - phi[i, j-1, k]) / (2*delta)

               if k == 0:
                   fz = -(phi[i, j, k+1] - phi[i, j, k]) / delta
               elif k == z-1:
                   fz = -(phi[i, j, k] - phi[i, j, k-1]) / delta
               else: 
                   fz =  -(phi[i, j, k+1] - phi[i, j, k-1]) / (2*delta)
                   
               force[i,j,k] = ((fx, fy, fz))
    return force


def accelerations(part, forcefield):
    for particle in part:
        x, y, z = particle[:3]
        i = int(x // l)
        j = int(y // l)
        k = int(z // l)
        particle[6:9] = forcefield[i, j, k]
    return part

def massProfile(part):
    r = np.sqrt((part[:, 0] - L / 2)**2 + (part[:, 1] - L / 2)**2 + (part[:, 2] - L / 2)**2) 
    rMax = np.max(r)
    points = np.linspace(0, rMax, 101)
    r0 = (points[:-1] + points[1:]) / 2  
    totalMass = []
    mass = 0
    for i in range(len(points) - 1):
        count = 0
        for radius in r:
            if points[i] <= radius < points[i + 1]:
                count += 1
        mass += count 
        totalMass.append(mass)

    return r0, totalMass

def accelerationProfile(part, t):
    r = np.zeros(Np)
    acc = np.zeros(Np)

    for n in range(Np):
        part1 = part[n]
        x = part1[0]
        y = part1[1]
        z = part1[2]
        ax = part1[6]
        ay = part1[7]
        az = part1[8]
        r[n] = np.sqrt((x-L/2)**2 + (y-L/2)**2 + (z-L/2)**2)
        acc[n] = np.sqrt(ax**2+ay**2 + az**2)
        
    radius, mass = massProfile(part)
    points = radius
    expectedA = (G* np.array(mass)) / points**2

    plt.figure(figsize=(10, 6))
    plt.scatter(r, acc, c='green', label='my acceleration')
    plt.plot(points, expectedA, color='black', label='expected acceleration')
    plt.title('accelerations comparison')
    plt.xlabel('radius m')
    plt.ylabel('accleration m/s^2')
    plt.legend()
    plt.show()

def visualizeParticles(part, t):
    radius, massprofile = massProfile(part)
    plt.figure(figsize=(12, 6))

    plt.scatter(part[:, 0], part[:, 1], s=2, c='blue')
    plt.title(f'xy positions at t/tdyn = {t:.2f}')
    plt.xlabel('x[m]')
    plt.ylabel('y[m]')
    plt.axis('square')
    plt.xlim(0, L)
    plt.ylim(0, L)
    plt.show()

    plt.figure(figsize=(12, 6))
    plt.scatter(part[:, 1], part[:, 2], s=2, c='red')
    plt.title(f'yz positions at t/tdyn = {t:.2f}')
    plt.xlabel('y[m]')
    plt.ylabel('z[m]')
    plt.axis('square')
    plt.xlim(0, L)
    plt.ylim(0, L)
    plt.show()
 
    plt.figure(figsize=(12, 6))
    plt.plot(radius, massprofile, c='green')
    plt.title('mass profile')
    plt.xlabel('radius [m]')
    plt.ylabel('cumulative mass [kg]')
    plt.show()
    accelerationProfile(part, t)

def timeIntegration(t0, tDynamical):
    part = initialConditions(Np)
    t = t0
    interval = tDynamical / 20
    count = 0

    while t < tDynamical and count < 20:
        density = densityF(part)
        phi = potential(density)
        forcefield = force(phi)
        part = accelerations(part, forcefield)

        tCurrent = t / tDynamical
        if count < t / interval:
            visualizeParticles(part, tCurrent)
            count += 1
            
        vmax = -1
        amax = -1

        for particle in part:
            vx, vy, vz = particle[3:6]
            vmag = np.sqrt(vx**2 + vy**2 + vz**2)
            if vmag > vmax:
                vmax = vmag

       
        for particle in part:
            ax, ay, az = particle[6:9]
            amag = np.sqrt(ax**2 + ay**2 + az**2)  
            if amag > amax:
                amax = amag
        
        dt = 0.5 * min(l / vmax, np.sqrt(l / amax))
        t += dt
        part[:, :3] += part[:, 3:6] * dt / 2 #dkd functionality 
        part[:, 3:6] += part[:, 6:9] * dt
        part[:, :3] += part[:, 3:6] * dt / 2

    visualizeParticles(part, tDynamical)

tDynamical = np.sqrt((np.pi**2 * Rsphere**3) / (4 * G * totalMass))
timeIntegration(t0, tDynamical)

#clear evolution in mass profile when
#compared to the inital one, as well as
#the evolution of the system under gravity

#Debugging:

L = 1 
Np = 1 
Nc = 128 
mp = 1 
G = 6.6743 * 10**-11  
part = np.zeros((Np, 9))  
density = np.zeros((Nc, Nc, Nc)) 

part = np.zeros((Np, 9))  
density = np.zeros((Nc, Nc, Nc)) 

def singleParticleTest(part, density, Nc, L, mp):
    l = L/Nc
    
    x, y, z = L/2 + l/2, L/2, L/2 #particle is placed

    i = int(x/l)
    j = int(y/l)
    k = int(z/l)
    
    dx = (x/l) -i
    dy = (y/l) - j
    dz = (z/l) - k

    dx_a  = [1-dx, dx]
    dy_b  = [1-dy, dy]
    dz_c  = [1-dz, dz]
    
    for a in range(len(dx_a)):
        for b in range(len(dy_b)):
            for c in range(len(dz_c)):
                i_a = i
                j_b = j
                k_c = k
                density[i_a, j_b, k_c] += mp * dx_a[a]* dy_b[b] * dz_c[c] / l**3
                
                print(f'density = {density[i_a, j_b, k_c]}', f'ia={i_a}', f'a={a}')
                print(f'density = {density[i_a, j_b, k_c]}', f'jb={j_b}', f'b={b}')
                print(f'density = {density[i_a, j_b, k_c]}', f'kc={k_c}', f'c={c}')
                print('\n')
    
    return density 

def potentialCalc(density, Nc, L, G):
    densityk = rfftn(density)
    wk = omegak(densityk.shape)
    potentialk = densityk * wk
    potential = irfftn(potentialk) * (L / Nc)**2
    return potential


def omegak(shape):
    Nkx, Nky, Nkz = shape
    Nk = Nkx
    wk = np.zeros((Nkx, Nky, Nkz))
    for i in range(Nkx):
        if i <= Nk //2:
            kx = 2*np.pi*i / Nk
        else:
            kx = 2*np.pi*(i-Nk) / Nk
        for j in range(Nky):
            if j <= Nk //2:
                ky = 2*np.pi*j / Nk
            else:
                ky = 2*np.pi*(j-Nk) / Nk
            for k in range(Nkz):
                kz = (2 * np.pi * k) / Nk
                if i == j == k == 0:
                    wk[i, j, k] = 0
                else:
                    wk[i, j, k] = -(4 * np.pi * G) / ((2 * np.sin(kx / 2))**2 + (2 * np.sin(ky / 2))**2 + (2 * np.sin(kz / 2))**2)
    return wk

def force(potential, Nc, L):
    x, y, z = potential.shape
    force = np.zeros((x, y, z, 3))
    delta = L/Nc
    fx = None
    fy = None
    fz = None
    for i in range(x):
        for j in range(y):
           for k in range(z):
               if i == 0:
                   fx = -(potential[i+1, j, k] - potential[i, j, k]) / delta
               elif i == x-1:
                   fx = -(potential[i, j, k] - potential[i-1, j, k]) / delta
               else: 
                   fx =  -(potential[i+1, j, k] - potential[i-1, j, k]) / (2*delta)

               if j == 0:
                   fy = -(potential[i, j+1, k] - potential[i, j, k]) / delta
               elif j == y-1:
                   fy = -(potential[i, j, k] - potential[i, j-1, k]) / delta
               else: 
                   fy =  -(potential[i, j+1, k] - potential[i, j-1, k]) / (2*delta)

               if k == 0:
                   fz = -(potential[i, j, k+1] - potential[i, j, k]) / delta
               elif k == z-1:
                   fz = -(potential[i, j, k] - potential[i, j, k-1]) / delta
               else: 
                   fz =  -(potential[i, j, k+1] - potential[i, j, k-1]) / (2*delta)
                   
               force[i,j,k] = ((fx, fy, fz))
    return force

def forceCheck(density, force, Nc, L, G, mp):
    potential = potentialCalc(density, Nc, L, G)
    forceF = force(potential, Nc, L)
    
    l = L/Nc
    x0 = np.array([L/2, L/2, L/2])
    rvalues = []
    fvalues = []

    for i in range(Nc):
         for j in range(Nc):
              for k in range(Nc):
                  pos = np.array([i*l, j*l, k*l])
                  rVector = pos - x0
                  r = np.sqrt(rVector[0]**2 + rVector[1]**2 + rVector[2]**2)
                  fVector = forceF[i,j,k]
                  f = np.sqrt(fVector[0]**2 + fVector[1]**2 + fVector[2]**2)

                  if r > 0:
                      rvalues.append(r)
                      fvalues.append(f)
                      
    rvalues = np.array(rvalues)
    fvalues = np.array(fvalues)
    
    plt.figure(figsize=(8,6))
    plt.plot(rvalues, fvalues, label='My Force')
    plt.xlabel("Radial Distance r")
    plt.ylabel("Force Magnitude f")
    plt.title("Check force (My Force)")
    plt.legend()
    plt.grid(True)
    plt.show()

    fexpected = G*mp/rvalues**2
    
    plt.figure(figsize=(8,6))
    plt.plot(rvalues, fexpected, color = 'green', label='Expected Force')
    plt.xlabel("Radial Distance r")
    plt.ylabel("Force Magnitude f")
    plt.title("Check force (Expected Force)")
    plt.legend()
    plt.grid(True)
    plt.show()

singleDensity = singleParticleTest(part, density, Nc, L, mp)
forceCheck(singleDensity, force, Nc, L, G, mp)
#My force agrees with what you would expect
#if you plotted newtons law, the density 
#values are also in agreement.
