# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:26:43 2018

@author: slavd
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
#from win32api import GetSystemMetrics

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
        self.decc = self.acc*4

    def FixPosition(width, length):
        pass
    
    def FindPosition(self, angle):
        return (self.radius*np.cos(angle), self.radius*np.sin(angle))
    
    def Draw(self, ax):
        self.artist = ax.add_patch(Rectangle(self.position, self.W, self.L, np.rad2deg(self.angle)))
#        if self.angle > 2*np.pi():
#            self.angle -= 2*np.pi()
        print(self.angle)
        return self.artist

    def CollisionWarning(self, next_car_angle):
        safe_distance = np.deg2rad(20)
        if self.angle + safe_distance >= next_car_angle:
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
            if self.speed >= 0:
                self.speed -= self.decc*dt
#            self.speed = 1

            
        self.angle += self.speed*dt
        self.position = self.FindPosition(self.angle)
        



fig1, ax1 = plt.subplots()
fig1.set_figheight(7)
fig1.set_figwidth(7)
#screen_width = GetSystemMetrics(0)
#screen_height = GetSystemMetrics(1)
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
#    last_vehicle = vehicles[0]
    for vehicle in vehicles:
#        if (len(vehicles) > 1):    
        for other_vehicle in vehicles:
            other_angle = other_vehicle.angle
            if other_vehicle == vehicle:
                vehicle.Drive(dt, 20)
            else:
                vehicle.Drive(dt, other_angle)
                    
                        
        artists.append(vehicle.Draw(ax1))
    return artists

def init():
    ax1.set_xlim(-4, 4)
    ax1.set_ylim(-4, 4)
    ax1.set_aspect(1)
    return []


anim = animation.FuncAnimation(fig1, animate, frames = totalFrames, interval = dt*1000, init_func = init, blit = True, repeat = False)
plt.show()