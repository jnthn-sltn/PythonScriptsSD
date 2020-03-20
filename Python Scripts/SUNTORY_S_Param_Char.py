# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 10:01:55 2019

@author: joslaton
"""

import os
import numpy as np
import skrf as rf
import pandas as pd

input_dir = r"C:\Users\joslaton\Documents\S-Params"

states2il_dict = {'LS_ASW_B1B3':4,
                  'LS_ASW_B7':3,
                  'LS_ASW_B41':2,
                  'LS_ASW_TRX1':5,
                  'LS_ASW_TRX2':6
                  }

rev_states2il_dict = dict(zip(list(states2il_dict.values()),list(states2il_dict.keys())))

states2iso_dict = {'LS_ASW_B1B3':[(4,i) for i in range(2,7) if i not in [4,6]],
                   'LS_ASW_B7':[(3,i) for i in range(2,7) if i not in [2,3]],
                   'LS_ASW_B41':[(2,i) for i in range(2,7) if i not in [2,3]],
                   'LS_ASW_TRX1':[(5,i) for i in range(2,7) if i not in [5,6]],
                   'LS_ASW_TRX2':[(6,i) for i in range(2,7) if i not in [4,5,6]]
                   }

freq_dict = {'1511MHz':1,
             '1995MHz':2,
             '2200MHz':3,
             '2400MHz':4,
             '2690MHz':5
             }

temperatures = {'-30C':-30,'25C':25,'85C':85}
voltages = {'1p15':1.15,'1p30':1.3,'1p35':1.35}

df_head_lst = ['Serial','Temperature','VDD','Thru']
df_head_lst += ['IL @ ' + el for el in list(freq_dict.keys())]
df_head_lst += ['WNAISO @ ' + el for el in list(freq_dict.keys())]
df_head_lst += ['RL @ ' + el for el in list(freq_dict.keys())]


#df = pd.DataFrame(columns=df_head_lst)


def filename_collector(fdir):
    a = []
    for root, dirs, files in os.walk(fdir):  
        for filename in files:
            if filename.endswith('p'):
                a += [root + '\\' +filename]
    return a

def status_tracker(a,b):
    c = float(a)/b
    print('\r{:.2%} Complete: {}/{}'.format(c,a,b))

fsrc_list = filename_collector(input_dir)

endarino = len(fsrc_list)

rows_list = []

for el in fsrc_list:
    d = {}
    tmp = el.split('\\')
    
    d['Serial'] = tmp[8].split('.')[0]
    d['Temperature'] = temperatures[tmp[6]]
    d['VDD'] = voltages[tmp[7]]
    d['Thru'] = tmp[5]
    tmpobj = rf.Network(el)
    for ele in df_head_lst[4:]:
        tmp2 = ele.split(' ')
        if tmp2[0]=='IL':
            d[ele] = tmpobj[1,states2il_dict[d['Thru']]][tmp2[2]].s_db[0,0,0]
        elif (tmp2[0]=='WNAISO'):
            d[ele] = np.max([tmpobj[band][tmp2[2]].s_db[0,0,0] for band in states2iso_dict[d['Thru']]])
        else:
            d[ele] = tmpobj[1,1][tmp2[2]].s_db[0,0,0]
    rows_list.append(d)
    status_tracker(len(rows_list),endarino)
    
df = pd.DataFrame(rows_list)

df.to_excel(input_dir+'\\'+'s-params_raw.xlsx',index=False)

#for el in fsrc_list:
#    tmp = el.split('\\')
#    temperatures += [tmp[10]]
#    voltages += [tmp[11]]
#    serials += [tmp[12].split('.')[0]]
#    
#
#
#temperatures = list(set(temperatures))
#voltages = list(set(voltages))
#serials = list(set(serials))
#
#
#
#
#class rf_record:
#   def __init__(self,state,temperature,voltage,serial):
#        self.state = state
#        self.temperature = temperature
#        self.voltage = voltage
#        self.serial = serial
#        self.path = p_string + '\\' + state + '\\' + temperature + '\\' + voltage + '\\' + serial + '.s13p'
#        self.rfobj = rf.Network(self.path)
#        self.rfobj.frequency.unit='MHz'
#        self.insertion_loss = [
#        self.iso = states2iso_dict[self.state]
#        






