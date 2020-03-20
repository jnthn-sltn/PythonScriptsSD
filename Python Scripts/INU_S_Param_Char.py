# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 14:18:00 2019

@author: joslaton
"""
import os
import numpy as np
import skrf as rf
import pandas as pd

input_dir = r"\\malibu\benchdata\1_Engineers\joslaton\INU\Char\S-Parameters"

states2il_dict = {'LS_ASW_B34_39':2,
                  'LS_ASW_B25_B66':3,
                  'LS_ASW_B1_B3':4,
                  'LS_ASW_B7':5,
                  'LS_ASW_B30':6,
                  'LS_ASW_B41':7,
                  'LS_ASW_TRX_2':8,
                  'LS_ASW_TRX_1':9,
                  'LS_ASW_B40':10,
           }
rev_states2il_dict = dict(zip(list(states2il_dict.values()),list(states2il_dict.keys())))
states2iso_dict = {
        'LS_ASW_B34_39':[(2,i) for i in range(2,11) if i not in [2,3]],
        'LS_ASW_B25_B66':[(3,i) for i in range(2,11) if i not in [2,3]],
        'LS_ASW_B1_B3':[(4,i) for i in range(2,11) if i not in [4,5]],
        'LS_ASW_B7':[(5,i) for i in range(2,11) if i not in [4,5,6]],
        'LS_ASW_B30':[(6,i) for i in range(2,11) if i not in [5,6,7]],
        'LS_ASW_B41':[(7,i) for i in range(2,11) if i not in [6,7,8]],
        'LS_ASW_TRX_2':[(8,i) for i in range(2,11) if i not in [7,8,9]],
        'LS_ASW_TRX_1':[(9,i) for i in range(2,11) if i not in [8,9,10]],
        'LS_ASW_B40':[(10,i) for i in range(2,11) if i not in [9,10]],
        }

freq_dict = {'800MHz':1,
          '1511MHz':2,
          '1995MHz':3,
          '2200MHz':4,
          '2400MHz':5,
          '2690MHz':6}

temperatures = {'-30C':-30,'25C':25,'85C':85}
voltages = {'1p50':1.5,'1p80':1.8,'2p10':2.1}

df_head_lst = ['Serial','Temperature','VDD','Thru']
df_head_lst += ['IL @ ' + el for el in list(freq_dict.keys())]
df_head_lst += ['WNAISO @ ' + el for el in list(freq_dict.keys())]
df_head_lst += ['RL @ ' + el for el in list(freq_dict.keys())]


#df = pd.DataFrame(columns=df_head_lst)


def filename_collector(fdir):
    a = []
    for root, dirs, files in os.walk(fdir):  
        for filename in files:
            a += [root + '\\' +filename]
    return a

def status_tracker(a,b):
    c = 100.0*float(a)/b
    print('\r' + str(c) + '% Complete: ' + str(a) + '/' + str(b))

fsrc_list = filename_collector(input_dir)

endarino = len(fsrc_list)

rows_list = []

for el in fsrc_list:
    d = {}
    tmp = el.split('\\')
    
    d['Serial'] = tmp[12].split('.')[0]
    d['Temperature'] = temperatures[tmp[10]]
    d['VDD'] = voltages[tmp[11]]
    d['Thru'] = tmp[9]
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

df.to_excel(input_dir+'\\'+'s-params_raw.xlsx')

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






