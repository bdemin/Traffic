# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 18:26:43 2018

@author: slavd
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Rectangle
from itertools import count

class Obj(object):
  _ids = count(0)

  def __init__(self):
    self.id = next(self._ids)


def CollisionCheck(current_vehicle, front_vehicle, dt):
#    print(np.rad2deg(veh1.angle))
#    print(np.rad2deg(veh2.angle),'\n')
    if (front_vehicle.angle - current_vehicle.angle) < np.deg2rad(10):
        print('Vehicle #', current_vehicle.ID, 'is Braking')
#              change color of a car which is braking or driving
        current_vehicle.Brake(dt)
    else:
        print('Vehicle #', current_vehicle.ID, 'is Driving')
        current_vehicle.Drive(dt)
            
class Vehicle(object):
    _ID = count(1)
    def __init__(self, radius):
        self.ID = next(self._ID)
        self.W = 0.1 *3
        self.L = 0.2 *3
        self.d = 0.5*((self.L**2+self.W**2)**0.5)
        self.alpha = np.arctan2(self.W, self.L)
        self.radius = radius
        
        self.angle = 0
        self.position = (self.radius-self.W/2, -self.L/2)
        self.speed = 0
        self.max_speed = (2*np.pi)/10
        self.acc = (2*np.pi)/16
        self.dec = self.acc * 2
        print('A Vehicle has Joined')

        
    def GetPosition(self, angle):
        x = self.radius*np.cos(angle) - self.d*np.cos(self.alpha)
        y = self.radius*np.sin(angle) - self.d*np.sin(self.alpha)
        return (x, y)
    
    def Draw(self, ax):
        self.AngleFix()
        self.artist = ax.add_patch(Rectangle(self.position, self.W, self.L, np.rad2deg(self.angle)))
        return self.artist


    def Drive(self, dt):
        if self.speed < self.max_speed:
            self.speed += self.acc*dt
        self.angle += self.speed*dt
        self.position = self.GetPosition(self.angle)
        
    def Brake(self, dt):
        if self.speed > 0:
            self.speed -= self.dec*dt
        self.angle += self.speed*dt
        self.position = self.GetPosition(self.angle)
        
    def AngleFix(self):
        if np.rad2deg(self.angle) > 360:
            self.angle -= np.deg2rad(360)
    
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
vehicles.append(Vehicle(radius))

#vehicles_sorted = []
#vehicles_sorted.append(Vehicle(radius))

num_vehicles = 0
T = 40
FPS = 48
totalFrames = T*FPS
dt = (1/FPS)

def animate(frame):
    artists = []
    
    if len(vehicles) == 1: #one vehicle existant
        vehicles[0].Drive(dt)
        artists.append(vehicles[0].Draw(ax1))
        
    else: #multiple vehicles
        vehicle_angles = []
        for vehicle in vehicles:
            vehicle_angles.append(vehicle.angle)
        vehicles_sorted = []
        vehicles_sorted = [x for _,x in sorted(zip(vehicle_angles, vehicles),
                                               key = lambda pair: pair[0])]
        
        for i in range(len(vehicles_sorted)-1):
            CollisionCheck(vehicles_sorted[i], vehicles_sorted[i+1], dt)
            
#            maybe I need to move everything here: create a loop over the vehicle range, sort the list, check all collisions and continue
            
            artists.append(vehicles[i].Draw(ax1))
        artists.append(vehicles[-1].Draw(ax1))

#        for vehicle in vehicles:    
#            artists.append(vehicle.Draw(ax1))
            
#    else:
#        for i in range(len(vehicles)):
#            for j in range(len(vehicles)):
#                if i!=j:
#                    CollisionCheck(vehicles[i], vehicles[j], dt)
#                    print(veh1.angle)
#                    print(veh2.angle)
#            artists.append(vehicles[i].Draw(ax1))
#    print('current time:', frame*dt, 'sec')
    return artists


def init():
    ax1.set_xlim(-4, 4)
    ax1.set_ylim(-4, 4)
    ax1.set_aspect(1)
    return []


anim = animation.FuncAnimation(fig1, animate, frames = totalFrames, interval = dt*1000, init_func = init, blit = True, repeat = False)

def press(event):
    if event.key == 'a':
        vehicles.append(Vehicle(radius))
#    sys.stdout.flush()

fig1.canvas.mpl_connect('key_press_event', press)

plt.show()