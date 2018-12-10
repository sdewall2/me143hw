# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 15:43:32 2018

@author: Stark
"""

from math import sin
from math import asin
from math import cos
from math import tan
from math import atan2
from math import sqrt


import numpy as np

#wind inputs : wn, we
#State inputs: Xidc, Xic, Hdc, Hc, Vac 
#State variables: pn, pe, Xid, Xi, hd, h, Va
#State calculated: psi
#State outputs:
#State tuning: bxd, bx, bhd, bh, bVa

class Aircraft:
    
    g = 1
    
    def __init__(self,wingspan,weight,b_i):
        self.wingspan = wingspan
        self.weight = weight
        self.u = np.array([[0],[0],[0],[0],[0]])
        self.x = np.array([[0],[0],[0],[0],[0],[0],[0]])
        self.psi = 0
        self.b = np.array([b_i[0],b_i[1],b_i[2],b_i[3],b_i[4]])
        
    def step(self,dt,x_old,u):
        w = np.array([0,0])
        np.seterr(divide='ignore', invalid='ignore')
        wn = w[1]
        we = w[0]
        pn = x_old[0][0]
        pe = x_old[1][0]
        Xid = x_old[2][0]
        Xi = x_old[3][0]
        hd = x_old[4][0]
        h = x_old[5][0]
        Va = x_old[6][0]

        Xidc = u[0]
        Xic = u[1]
        hdc = u[2]
        hc = u[3]
        Vac = u[4]
        
        if (Va>1):
            temp = (1/Va)*np.dot(np.array([[wn],[we]]).T,np.array([[-sin(Xi)],[cos(Xi)]]))
        else:
            temp = 0
        psi = Xi - asin(temp)
        
        pnd = Va*cos(psi) + wn
        ped = Va*sin(psi) + we
        Xidd = self.b[0]*(Xidc-Xid)+self.b[1]*(Xic-Xi)
        hdd = self.b[2]*(hdc-hd)+self.b[3]*(hc-h)
        Vad = self.b[4]*(Vac-Va)
        
        pn = pn + pnd*dt
        pe = pe + ped*dt
        Xi = Xi + Xid*dt
        Xid = Xid + Xidd*dt
        h = h + hd*dt
        hd = hd + hdd*dt
        Va = Va + Vad*dt
        
        xd_new = np.array([[pnd],[ped],[Xidd],[Xid],[hdd],[hd],[Vad]])
        x_new = np.array([[pn],[pe],[Xid],[Xi],[hd],[h],[Va]])
        
        return x_new,psi,xd_new
        