# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 14:12:06 2019

@author: joslaton
"""

import skrf as rf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%       

p_string =r"\\malibu\benchdata\1_Engineers\joslaton\****\TURKISH_SKEW\S-Parameters\ES3.1"
output_path = r"\\malibu\benchdata\1_Engineers\joslaton\****\TURKISH_SKEW\S-Parameters\ES3.1\ALL"
states = ['LS_TX_IN1_TX_OUT1',
          'LS_TX_IN2_TX_OUT1',
          'LS_TX_IN1_TX_OUT2',
          'LS_TX_IN2_TX_OUT2']
temperatures = ['-35C','25C','85C']
voltages = ['3p30',
            '3p15',
            '3p02']

s_dict = dict(zip(states,range(len(states))))
rev_sdict = dict(zip(range(len(states)),states))
t_dict = dict(zip(temperatures,range(len(temperatures))))
rev_tdict = dict(zip(range(len(temperatures)),temperatures))
v_dict = dict(zip(voltages,range(len(voltages))))
rev_vdict = dict(zip(range(len(voltages)),voltages))

il_dict = {0:'s31',
           1:'s32',
           2:'s41',
           3:'s42'}
 

serials = ['POR SN1','POR SN2','POR SN3',
           'SSSS SN1','SSSS SN2','SSSS SN3',
           'FFFF SN1','FFFF SN2','FFFF SN3']
#%%
###############################################################################

class rf_record:
   def __init__(self,state,temperature,voltage,serial):
        self.state = state
        self.temperature = temperature
        self.voltage = voltage
        self.serial = serial
        self.path = p_string + '\\' + state + '\\' + temperature + '\\' + voltage + '\\' + serial + '.s4p'
        self.rfobj = rf.Network(self.path)
        self.row = v_dict[self.voltage]
        self.col = t_dict[self.temperature]
        self.rfobj.frequency.unit='ghz'
        self.iso_out_out = self.rfobj.s34
        self.iso_in_in = self.rfobj.s12
        if s_dict[self.state]==0:
            self.insertion_loss = self.rfobj.s31
            self.iso_io_label = 'ISO IN1-OUT2'
            self.iso_oi_label = 'ISO IN2-OUT1'
            self.iso_in_out = self.rfobj.s14
            self.iso_out_in = self.rfobj.s32
        elif s_dict[self.state]==1:
            self.insertion_loss = self.rfobj.s32
            self.iso_io_label = 'ISO IN2-OUT2'
            self.iso_oi_label = 'ISO IN1-OUT1'
            self.iso_in_out = self.rfobj.s24
            self.iso_out_in = self.rfobj.s31
        elif s_dict[self.state]==2:
            self.insertion_loss = self.rfobj.s41
            self.iso_io_label = 'ISO IN1-OUT1'
            self.iso_oi_label = 'ISO IN2-OUT2'
            self.iso_in_out = self.rfobj.s13
            self.iso_out_in = self.rfobj.s42
        else:
            self.insertion_loss = self.rfobj.s42
            self.iso_io_label = 'ISO IN2-OUT1'
            self.iso_oi_label = 'ISO IN1-OUT2'
            self.iso_in_out = self.rfobj.s23
            self.iso_out_in = self.rfobj.s41

###############################################################################
#%%
a = []

for state in states:
    for temperature in temperatures:
        for voltage in voltages:
            for serial in serials:
                a += [rf_record(state,temperature,voltage,serial)]
#%%
b = [rec for rec in a if 'FFFF' in rec.serial]#) and ('SN1' not in rec.serial))]#all([rec.serial!='SN1',rec.serial!='SN2'])]

fig_0, axes_0 = plt.subplots(3, 3)
fig_1, axes_1 = plt.subplots(3, 3)
fig_2, axes_2 = plt.subplots(3, 3)
fig_3, axes_3 = plt.subplots(3, 3)

fig_0.suptitle('FFFF IN1_OUT1: Insertion Loss')
fig_1.suptitle('FFFF IN2_OUT1: Insertion Loss')
fig_2.suptitle('FFFF IN1_OUT2: Insertion Loss')
fig_3.suptitle('FFFF IN2_OUT2: Insertion Loss')

fig_lst = [fig_0,fig_1,fig_2,fig_3]

ax_lst = [axes_0,axes_1,axes_2,axes_3]

for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_title('Voltage: ' + rev_vdict[i] + ', Temp: ' + rev_tdict[j])
            ax[i,j].plot(range(10000000,4100000000,5000000),[-1]*818,'r',label='Spec_Line')
            #ax[i,j].set_ylim(bottom=-1.2,top=-0.3)

    
#%%
#Insertion Loss Plotter
for el in b:
    el.insertion_loss['0.01-4.1ghz'].plot_s_db(ax=ax_lst[s_dict[el.state]][el.row,el.col],label=el.serial+', IL')

#%%
for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_ylim(bottom=-1.2,top=-0.3)

for fig in fig_lst:
    fig.set_size_inches((18.81,9.3),forward=False)
    fig.subplots_adjust(top=0.928,bottom=0.061,left=0.041,right=0.99,hspace=0.338,wspace=0.147)
    fig.savefig(output_path +'\\'+ fig.texts[0].get_text().replace(': ',' - ') + '.jpg')

#%%
plt.close(fig='all')

            
#%%
b = [rec for rec in a if 'FFFF' in rec.serial]# if all([rec.serial!='SN1',rec.serial!='SN2'])]

fig_0, axes_0 = plt.subplots(3, 3)
fig_1, axes_1 = plt.subplots(3, 3)
fig_2, axes_2 = plt.subplots(3, 3)
fig_3, axes_3 = plt.subplots(3, 3)

fig_0.suptitle('FFFF IN1_OUT1: Iso')
fig_1.suptitle('FFFF IN2_OUT1: Iso')
fig_2.suptitle('FFFF IN1_OUT2: Iso')
fig_3.suptitle('FFFF IN2_OUT2: Iso')

fig_lst = [fig_0,fig_1,fig_2,fig_3]

ax_lst = [axes_0,axes_1,axes_2,axes_3]

for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_title('Voltage: ' + rev_vdict[i] + ', Temp: ' + rev_tdict[j])
            ax[i,j].plot(range(10000000,4100000000,5000000),[-30]*818,linestyle=':',color='r',label='Spec_Line_30dB')
            ax[i,j].plot(range(10000000,4100000000,5000000),[-55]*818,linestyle=':',color='r',label='Spec_Line_55dB')
            #ax[i,j].set_ylim(bottom=-1.2,top=-0.3)

#%%

for el in b:
    el.iso_out_out['0.01-4.1ghz'].plot_s_db(ax=ax_lst[s_dict[el.state]][el.row,el.col],label=el.serial+', ISO OUT1-OUT2')
    el.iso_in_in['0.01-4.1ghz'].plot_s_db(ax=ax_lst[s_dict[el.state]][el.row,el.col],label=el.serial+', ISO IN1-IN2')
    el.iso_in_out['0.01-4.1ghz'].plot_s_db(ax=ax_lst[s_dict[el.state]][el.row,el.col],label=el.serial+', '+ el.iso_io_label)
    el.iso_out_in['0.01-4.1ghz'].plot_s_db(ax=ax_lst[s_dict[el.state]][el.row,el.col],label=el.serial+', '+ el.iso_oi_label)
    
    


#%%
for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_ylim(bottom=-80,top=-20)
            ax[i,j].legend(loc='lower right',fontsize='xx-small')
#%%
for fig in fig_lst:
    fig.set_size_inches((18.81,9.3),forward=False)
    fig.subplots_adjust(top=0.928,bottom=0.061,left=0.041,right=0.99,hspace=0.338,wspace=0.147)
    fig.savefig(output_path +'\\'+ fig.texts[0].get_text().replace(': ',' - ') + '.jpg')

#%%
plt.close(fig='all')
#%%

nominal = [rec for rec in a if all(['FFFF' in rec.serial,rec.temperature==rev_tdict[1],rec.voltage==rev_vdict[1]])]
wc = [rec for rec in a if all(['FFFF' in rec.serial,rec.temperature==rev_tdict[2],rec.voltage==rev_vdict[0]])]

#%%
nom_ary = np.zeros([4,6])
wc_ary = np.zeros([4,6])


i1o1 = rf.average([rec.rfobj for rec in nominal if (rec.state==rev_sdict[0])])
i2o1 = rf.average([rec.rfobj for rec in nominal if (rec.state==rev_sdict[1])])
i1o2 = rf.average([rec.rfobj for rec in nominal if (rec.state==rev_sdict[2])])
i2o2 = rf.average([rec.rfobj for rec in nominal if (rec.state==rev_sdict[3])])
k = 0
for ntwrk in [i1o1,i2o1,i1o2,i2o2]:
    nom_ary[k,:] = [ntwrk.s31['2.7GHz'].s_db[0,0,0],
                    ntwrk.s32['2.7GHz'].s_db[0,0,0],
                    ntwrk.s41['2.7GHz'].s_db[0,0,0],
                    ntwrk.s42['2.7GHz'].s_db[0,0,0],
                    ntwrk.s21['2.7GHz'].s_db[0,0,0],
                    ntwrk.s43['2.7GHz'].s_db[0,0,0]]
    k+=1


#%%

i1o1 = rf.average([rec.rfobj for rec in wc if (rec.state==rev_sdict[0])])
i2o1 = rf.average([rec.rfobj for rec in wc if (rec.state==rev_sdict[1])])
i1o2 = rf.average([rec.rfobj for rec in wc if (rec.state==rev_sdict[2])])
i2o2 = rf.average([rec.rfobj for rec in wc if (rec.state==rev_sdict[3])])
k = 0
for ntwrk in [i1o1,i2o1,i1o2,i2o2]:
    wc_ary[k,:] = [ntwrk.s31['2.7GHz'].s_db[0,0,0],
                    ntwrk.s32['2.7GHz'].s_db[0,0,0],
                    ntwrk.s41['2.7GHz'].s_db[0,0,0],
                    ntwrk.s42['2.7GHz'].s_db[0,0,0],
                    ntwrk.s21['2.7GHz'].s_db[0,0,0],
                    ntwrk.s43['2.7GHz'].s_db[0,0,0]]
    k+=1


#%%
np.savetxt(output_path + '\\' + 'Nominal Small Signal.txt',nom_ary,delimiter=',')
np.savetxt(output_path + '\\' + 'WC Small Signal.txt',wc_ary,delimiter=',')










