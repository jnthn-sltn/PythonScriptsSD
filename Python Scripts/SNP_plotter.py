# -*- coding: utf-8 -*-


import matplotlib.pyplot as plt
import pandas as pd
import skrf as rf
import os




def filename_collector(fdir,ftype):
    a = []
    for root, dirs, files in os.walk(fdir):  
        for filename in files:
            if filename.split('.')[-1]==ftype:
                a += [root + '\\' +filename]
    return a




class device_record:
    def __init__(self,path):
        self.path=path
        self.net = rf.Network(path)
        nemsplit = self.net.name.split('_')
        self.state= nemsplit[2] + nemsplit[4]
        self.serial = nemsplit[7]
        self.vdd=nemsplit[8]
        self.temperature= self.path.split('\\')[-2]
        self.net.name=self.serial




fdir =r'\\malibu\benchdata\1_Engineers\joslaton\WOLF\WOLF_ES2cpy\WOLF_Spara'




paths = filename_collector(fdir,'s4p')




record_holder = [device_record(path) for path in paths]




states = sorted(list(set([rec.state for rec in record_holder])))
#serials = list(set([rec.serial for rec in record_holder]))
serials = ['SN8', 'SN9', 'SN10', 'SN3', 'SN4']
voltages = sorted(list(set([rec.vdd for rec in record_holder])))
temperatures = sorted(list(set([rec.temperature for rec in record_holder])))




fig11,axes11=plt.subplots(3,3,sharex='col',sharey='row')
fig21,axes21=plt.subplots(3,3,sharex='col',sharey='row')
fig12,axes12=plt.subplots(3,3,sharex='col',sharey='row')
fig22,axes22=plt.subplots(3,3,sharex='col',sharey='row')




fig_dict = dict(zip(states,[fig11.number,fig12.number,fig21.number,fig22.number]))
row_dict = dict(zip(voltages,[3,2,1]))
col_dict = dict(zip(temperatures,[1,2,3]))
style_dict = {"SN8":'-',"SN9":'-',"SN10":'-',"SN3":'-.',"SN4":'-.'}







