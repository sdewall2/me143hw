# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 17:46:42 2018

@author: Stark
"""

import numpy as np


#Define Phases of Flight
def flight_plan(argument):
    plan = {
            0:"DEAD",
            1:"Arming",
            2:"Launch",
            3:"Loiter",
            4:"Free",
            5:"Landing",
            6:"Flare",
            7:"Landed"
            }
    return plan.get(argument,'Invalid')


class FlightPlan:
    
    def __init__(self):
        self.SM = flight_plan(1)
        self.current_state_tstart = 0
        print(self.SM)
        
    #Only changes the SM and the start time of each phase
    def check_triggers(self,t,x):
        altitude = x[5][0]
        if (altitude<0):
            if self.SM != "DEAD":
                self.SM = flight_plan(0)
                print "Crashed into the dirt"
            
        if (self.SM == "Arming"):
            if ((t-self.current_state_tstart)>10):
                self.SM = flight_plan(2)
                self.current_state_tstart = t
                print "Launching"
        
        if (self.SM == "Launch"):
            if (altitude) > 95:
                self.SM = flight_plan(4)
                print "Reached Altitude" 
                self.current_state_tstart = t
                
        if (self.SM=="Free"):
            if (t-self.current_state_tstart)> 120:
                self.SM = "Landing"
                print "Landing"
        
        if (self.SM=="Landing"):
            if (altitude < 15):
                self.SM = flight_plan(6)
                print "Flaring"
                
        if (self.SM=="Flare"):
            if (altitude < 1):
                self.SM = flight_plan(7)
                print "Landed"
        
    def state_function(self,t,dt,x):
        if self.SM == "DEAD":
            u = np.array([0,0,0,0,0])
            
        if self.SM == "Arming":
            u = np.array([0,0,0,0,.010])
        
        if self.SM == "Launch":
            altitude = x[5][0]+100*dt
            u = np.array([0,0,0,altitude,8])
        
        if self.SM == "Free":
            u = np.array([0,.2,0,100,4])
    
        if self.SM == "Landing":
            altitude = x[5][0]-100*dt
            u = np.array([0,0,0,altitude,4])
            #print(altitude)
        
        if self.SM == "Flare":
            altitude = x[5][0]-10*dt
            u = np.array([0,0,0,altitude,4])
            #print(altitude)
    
        if self.SM == "Landed":
            u = np.array([0,0,0,0,0])
        
        return u
    


    
    