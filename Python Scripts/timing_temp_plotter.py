# -*- coding: utf-8 -*-
"""
Created on Fri Jan  3 15:28:04 2020

@author: joslaton
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def filename_collector(fdir):
    a = []
    for root, _, files in os.walk(fdir):  
        for filename in files:
            if filename.endswith('v'):
                a += [root + '\\' +filename]
    return a

#idx1=100
#idx2=150
#idx3=200
def linearity_edge_finder(xf,yf,idx1,idx2,idx3):
    nf = np.mean(yf[idx2:idx3]) #150-200
    #nf_std = np.std(yf[idx2:idx3]) #150-200
    nf_sig = nf+6#3*nf_std
    xf=xf[idx1:idx2] #100-150
    yf=yf[idx1:idx2] #100-150
    i=0
    while yf[234+i]>nf_sig:
        i += 1
    #print(xf[157])
    return [xf[234+i]-xf[157]]
    
    
#1000=0
#1781=50    
#2562=100
#3343=150
#4125=200
#4906=250
#5687=300
#6468=350
#7250=400

in_file=r"****"
flist = filename_collector(in_file)
onoff_list = []
offon_list = []

for file in flist:
    t_df = pd.read_csv(file,header=10)
    x = t_df['time(us)'].values
    y = t_df['power(dBm)'].values
    offon_list += linearity_edge_finder(x,y,1000,1781,2562)
    onoff_list += linearity_edge_finder(x,y,2562,3343,4125)
    offon_list += linearity_edge_finder(x,y,4125,4906,5687)
    onoff_list += linearity_edge_finder(x,y,5687,6468,7250)
    
    
    
#    print(xf[237+i])
#    print(nf_sig)
#    plt.plot(xf, yf, '-', xf[237+i], yf[237+i], 'ro')
#    plt.show()
