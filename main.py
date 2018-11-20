# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:26:43 2018

@author: slavd
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
import numpy as np

class Vehicle(object):
    def __init__(self, radius):
        self.W = 0.1
        self.L = 0.2
        self.radius = radius
        
        self.angle = 0
        self.position = (self.radius, 0)
        self.speed = 0
        self.max_speed = 2*np.pi/4
        self.acc = 2*np.pi/16

        
    def FindPosition(self, angle):
        return (self.radius*np.cos(angle), self.radius*np.sin(angle))
    
    def Draw(self, ax):
        self.artist = ax.add_patch(Rectangle(self.position, self.W, self.L, np.rad2deg(self.angle)))
        return self.artist

    def CollisionWarning(self, next_car_angle):
        if self.angle < next_car_angle + np.deg2rad(10):
            return True
        else:
            return False


    def Drive(self, dt, next_car_angle):
        if not self.CollisionWarning(next_car_angle):
            if self.speed < self.max_speed:
                print('vroom')
                self.speed += self.acc*dt
        else:
            print('brake!')
            self.speed -= self.acc*dt

            
        self.angle += self.speed*dt
        self.position = self.FindPosition(self.angle)
        
    
#    def SlowDown(self):
#        self.angle -= self.acc
#        self.position = self.FindPosition(self.angle)

    

    
    def FixPosition(width, length):
        pass
    
    
#fig1 = plt.figure(figsize=(28, 18), facecolor='w', edgecolor='g')
#ax1 = plt.axes(xlim=(-5, 5), ylim=(-5, 5))
#plt.xlim(-5,5)
#plt.ylim(-5,5)
#plt.axis('equal')
#plt.axis([-3, 3, -3, 3])

fig1, ax1 = plt.subplots()

#fig1.set_size_inches(w = 8, h = 8)
radius = 3


vehicles = []
T = 40
FPS = 48
totalFrames = T*FPS
dt = (1/FPS)

def animate(frame):
    print('current time:', frame*dt, 'sec')
    artists = []
    if (len(vehicles) < 2) and (frame % 100 == 0):
        vehicles.append(Vehicle(radius))
    
#    draw all
    last_vehicle = vehicles[0]
    for vehicle in vehicles:
        artists.append(vehicle.Draw(ax1))
#        print(vehicle.position,'\n')
#        print(vehicle.angle,'\n')
        vehicle.Drive(dt, last_vehicle.angle)
        last_vehicle = vehicle
    return artists

def init():
    ax1.set_xlim(-4, 4)
    ax1.set_ylim(-4, 4)
    ax1.set_aspect(1)
    return []


anim = animation.FuncAnimation(fig1, animate, frames = totalFrames, interval = dt*1000, init_func = init, blit = True, repeat = False)
plt.show()