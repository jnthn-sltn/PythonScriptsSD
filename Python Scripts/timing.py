# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 15:10:42 2020

@author: joslaton
"""
import os
import pandas as pd
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

def filename_collector(fdir):
    a = []
    for root, dirs, files in os.walk(fdir):  
        for filename in files:
            if filename.endswith('v'):
                a += [root + '\\' +filename]
    return a

def status_tracker(a,b):
    c = float(a)/b
    print('\r{:.2%} Complete: {}/{}'.format(c,a,b))

def rising_edge_1dB_finder(filelist):
    try:
        val_list = []
        i=0
        for file in filelist:
            t_df = pd.read_csv(file,header=10)
            x = t_df['time(us)'].values
            y = t_df['power(dBm)'].values
            fin_ave = np.mean(y[-10:])-1
            f=interpolate.interp1d(y,x)
            val_list += [f(fin_ave).tolist()]
            i += 1
            status_tracker(i,len(filelist))
        return val_list
    except:
        print(file)

def falling_edge_1dB_finder(filelist):
    try:
        val_list = []
        i=0
        for file in filelist:
            t_df = pd.read_csv(file,header=10)
            x = np.flip(t_df['time(us)'].values)
            y = np.flip(t_df['power(dBm)'].values)
            fin_ave = np.mean(y[-10:])-1
            f=interpolate.interp1d(y,x)
            val_list += [f(fin_ave).tolist()]
            i += 1
            status_tracker(i,len(filelist))
        return val_list
    except:
        print(file)

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

def linearity_timing_finder(filelist):
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
    
    return (onoff_list,offon_list)
    


root_dir = r"****"

flist = filename_collector(root_dir)

#value_list = rising_edge_1dB_finder(flist)
#value_list = falling_edge_1dB_finder(flist)
value_list1,value_list2 = linearity_timing_finder(flist)


val_mean = np.mean(value_list2)
val_std = np.std(value_list2)
val_plus = val_mean + 6*val_std

print('\nOFFONMean: {:.4} \n'.format(val_mean))
print('OFFONstd: {:.3} \n'.format(val_std))
print('OFFONMean+6*std: {:.4} \n'.format(val_plus))

val_mean = np.mean(value_list1)
val_std = np.std(value_list1)
val_plus = val_mean + 6*val_std

print('\nONOFFMean: {:.4} \n'.format(val_mean))
print('ONOFFstd: {:.3} \n'.format(val_std))
print('ONOFFMean+6*std: {:.4} \n'.format(val_plus))

#for file in filelist:
#    t_df = pd.read_csv(file,header=10)
#    x = t_df['time(us)'].values
#    y = t_df['power(dBm)'].values
#    fin_ave = np.mean(y[-10:])-1
#    yreduced = y - fin_ave
#    freduced=interpolate.UnivariateSpline(x,yreduced,s=0)
#    val_list += [freduced.roots()[0]]
#    i += 1
#    status_tracker(i,len(filelist))


#t_df = pd.read_csv(filelist[1],header=10)
#x = t_df['time(us)'].values
#y = t_df['power(dBm)'].values
#fin_ave = np.mean(y[-10:])-1
##yreduced = y - fin_ave
#f=interpolate.interp1d(x,y,bounds_error=False,fill_value="extrapolate")
#xnew = np.arange(-10.0,30.0,0.025)
#ynew=f(xnew)
#plt.plot(x, y, 'o', xnew, ynew, '-')
#plt.show()

#t_df = pd.read_csv(filelist[1],header=10)
#x = t_df['time(us)'].values
#y = t_df['power(dBm)'].values
#fin_ave = np.mean(y[-10:])-1
##yreduced = y - fin_ave
#f=interpolate.UnivariateSpline(x,y,s=0)
#xnew = np.arange(-10.0,30.0,0.025)
#ynew=f(xnew)
#plt.plot(x, y, 'o', xnew, ynew, '-')
#plt.show()
