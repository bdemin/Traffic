# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:26:43 2018

@author: slavd
"""

import matplotlib.pyplot as plt
#import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np

class Vehicle(object):
    def __init__(self):
        self.W = 0.1
        self.L = 0.2
        self.rad = 4
        self.angle = 0
        self.position = (self.rad, 0)
        self.speed = 0
        self.acc = 100
        
    def FindPosition(self, angle):
        return (self.rad*np.cos(np.deg2rad(angle)), self.rad*np.sin(np.deg2rad(angle)))
    
    def Draw(self):
        return Rectangle(self.position, self.W, self.L, self.angle)

    def Drive(self, dt):
        if self.speed < 300:
            self.speed += self.acc*dt
        self.angle += self.speed*dt
        self.position = self.FindPosition(self.angle)
        
    
    def SlowDown(self):
        self.angle -= self.acc
        self.position = self.FindPosition(self.angle)

    
    def CollisionWarning(self, next_car_angle):
        if self.angle < next_car_angle+10:
            self.SlowDown()
    
    
fig1 = plt.figure(figsize=(28, 18), facecolor='w', edgecolor='g')
ax1 = plt.axes(xlim=(-5, 5), ylim=(-5, 5))
#plt.xlim(-5,5)
#plt.ylim(-5,5)
#plt.axis('equal')
#plt.axis([-3, 3, -3, 3])



T = 5
dt = 0.05
N = int(T/dt)
vehicles = []
for t in range(N):
    ax1.cla()
    if (len(vehicles) < 5) and (t % 10 == 0):
        vehicles.append(Vehicle())
        
#    draw all
    for vehicle in vehicles:
        ax1.add_patch(vehicle.Draw())
        vehicle.Drive(dt)
#        plt.axis('equal')
        plt.xlim(-5,5)
        plt.ylim(-5,5)
#        print(vehicle.position,'\n')
#        print(vehicle.angle,'\n')
    plt.pause(1/60)
    
    
#    for vehicle in vehicles:
        
    
#    ax1.cla()

    
#for i in range(N):






#def animfunc(i):
#    vehicle_size = (0.1,0.1)
#    vehicle_pos = (0,-vehicle_size[0]/2)
#    c1 = Rectangle(vehicle_pos,height = vehicle_size[0], width = vehicle_size[1])
#    ax1.add_patch(c1)
#    return c1,
#    
#line_ani = animation.FuncAnimation(fig1, animfunc, frames = 100,
#                                   interval=80, blit=False)
#plt.show()