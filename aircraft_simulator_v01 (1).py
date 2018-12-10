# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from Aircraft import Aircraft
from flight_planner import FlightPlan

import random
import numpy as np
np.errstate(divide='ignore')
import matplotlib.pyplot as plt
from math import sin
from math import cos

time_end = 350
dt = 0.05



t = 0
wingspan = 10
weight = 5
#State tuning: bxd, bx, bhd, bh, bVa
b_i = np.array([.9,.2,.6,.2,.1])

myAircraft1 = Aircraft(wingspan,weight,b_i)
myFlightPlan = FlightPlan()

#State variables: pn, pe, Xid, Xi, hd, h, Va
x = np.array([[0],[0],[0],[0],[0],[0],[0]])
#wind inputs : wn, we
w = np.array([0,0])
#State inputs: CourseDerivative, Course (rads), Altitude Derivative, Altitude, Airspeed 
u = np.array([                0,            .1,                   0,      100,      12])

steps = int(time_end/dt)
psi_array = np.zeros(steps)
pn_array = np.zeros(steps)
pe_array = np.zeros(steps)
h_array = np.zeros(steps)
u_h_array = np.zeros(steps)
w_array = np.zeros(steps)
i=0


while t < time_end:
    
    #NO CHANGING
    #This defines how to transition to each phase of flight
    myFlightPlan.check_triggers(t,x)
        
    #This defines what to do during each phase of flight    
    u = myFlightPlan.state_function(t,dt,x)
     
    #This updates the aircraft position each time step   
    x_new, psi, xd_new = myAircraft1.step(dt,x,u)
    #NO CHANGING
    
    psi_array[i] = psi
    pn_array[i] = x_new[0][0]
    pe_array[i] = x_new[1][0]
    h_array[i] = x_new[5][0]
    u_h_array[i] = u[3]
    
    #NO CHANGING
    x = x_new
    t = t+dt
    i=i+1
    #NO CHANGING
    

#Plot the heading angle
t_plot = np.linspace(0.0, float(time_end),steps)
plt.plot(t_plot,np.degrees(psi_array))
plt.xlabel('Time (s)')
plt.ylabel('Heading (degrees)')
plt.title("Aircraft Heading")
plt.show()


#%%

#Plot the Altitude and desired altitude
fig = plt.figure()
alt, = plt.plot(t_plot,h_array, label='Altitude')
comm, = plt.plot(t_plot,u_h_array,'r--',label='Commanded')
ax = plt.gca()
ax.axis('scaled')
plt.xlabel('Time (s)')
plt.ylabel('Altitude (m)')
plt.title('Flight Altitude')
plt.legend(handles=[alt,comm])

fig = plt.gcf()
fig.set_size_inches(10, 5)
fig.savefig('output_flight_altitude.png', dpi=300)

#Plot the flight path
fig = plt.figure()
plt.plot(pe_array,pn_array)
ax = plt.gca()
ax.axis('scaled')
plt.xlabel('East (m)')
plt.ylabel('North (m)')
plt.title('Flight Altitude')
fig = plt.gcf()
fig.set_size_inches(5, 10)
fig.savefig('output_flight_path.png', dpi=300)



