# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 16:39:53 2019

@author: joslaton
"""

import pandas as pd
import pathlib
import os


def filename_collector(fdir):
    a = []
    for root, dirs, files in os.walk(fdir):  
        for filename in files:
            a += [root + '\\' +filename]
    return a

def file_mapper(flist_dst):
    dir_lst = list(set(['\\'.join(el.split('\\')[:-1]) for el in flist_dst]))
    for el in dir_lst:
        pathlib.Path(el).mkdir(parents=True, exist_ok=True)

def status_tracker(a,b):
    c = float(a)/b
    print('\r{:.2%} Complete: {}/{}'.format(c,a,b))

def spur_finder(src):
    d = {}
    i = 0
    ender = len(src)
    for fname in src:
        i+=1
        tmp_df = pd.read_csv(fname,header=9)
        m = tmp_df['power(dBm)'].max()
        if (m>-120):
            d[fname] = m
        status_tracker(i,ender)
    return d

input_path = r"\\malibu\benchdata\1_Engineers\joslaton\SHIBA\CHAR\RX Spur\Shiba_ASW_RX_Spur_TRACE_DATA"

#%%
flist_src = filename_collector(input_path)

#%%
spur_dict = spur_finder(flist_src)

#%%
df = pd.DataFrame([list(spur_dict.keys()),list(spur_dict.values())]).transpose()

#%%
df.to_excel(input_path+'.xlsx',index=False)
