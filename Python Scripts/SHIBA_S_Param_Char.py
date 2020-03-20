# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 14:41:29 2019

@author: joslaton
"""

import os
import numpy as np
import skrf as rf
import pandas as pd

input_dir = r"\\malibu\benchdata\1_Engineers\joslaton\SHIBA\CHAR\S-Parameters"

states2il_dict = {'LS_ANT1_SWOUT1_B3':3,
                  'LS_ANT1_SWOUT2_B7':4,
                  'LS_ANT1_SWOUT3_B41':5,
                  'LS_ANT1_SWOUT4_B40':6,
                  'LS_ANT1_SWOUT5_TRX1':7,
                  'LS_ANT1_SWOUT6_TRX2':8,
                  'LS_ANT2_SWOUT1_B3':3,
                  'LS_ANT2_SWOUT2_B7':4,
                  'LS_ANT2_SWOUT3_B41':5,
                  'LS_ANT2_SWOUT4_B40':6,
                  'LS_ANT2_SWOUT5_TRX1':7,
                  'LS_ANT2_SWOUT6_TRX2':8}

rev_states2il_dict = dict(zip(list(states2il_dict.values()),list(states2il_dict.keys())))

states2iso_dict = {'LS_ANT1_SWOUT1_B3':[(3,i) for i in range(3,9) if i not in [3]],
                  'LS_ANT1_SWOUT2_B7':[(4,i) for i in range(3,9) if i not in [4]],
                  'LS_ANT1_SWOUT3_B41':[(5,i) for i in range(3,9) if i not in [5]],
                  'LS_ANT1_SWOUT4_B40':[(6,i) for i in range(3,9) if i not in [6]],
                  'LS_ANT1_SWOUT5_TRX1':[(7,i) for i in range(3,9) if i not in [7]],
                  'LS_ANT1_SWOUT6_TRX2':[(8,i) for i in range(3,9) if i not in [8]],
                  'LS_ANT2_SWOUT1_B3':[(3,i) for i in range(3,9) if i not in [3]],
                  'LS_ANT2_SWOUT2_B7':[(4,i) for i in range(3,9) if i not in [4]],
                  'LS_ANT2_SWOUT3_B41':[(5,i) for i in range(3,9) if i not in [5]],
                  'LS_ANT2_SWOUT4_B40':[(6,i) for i in range(3,9) if i not in [6]],
                  'LS_ANT2_SWOUT5_TRX1':[(7,i) for i in range(3,9) if i not in [7]],
                  'LS_ANT2_SWOUT6_TRX2':[(8,i) for i in range(3,9) if i not in [8]],}

freq_dict = {'800MHz':1,
          '1511MHz':2,
          '1995MHz':3,
          '2200MHz':4,
          '2400MHz':5,
          '2690MHz':6}

temperatures = {'-30C':-30,'25C':25,'85C':85,'AMB':25}
voltages = {'1p50':1.5,'1p80':1.8,'2p20':2.2}

df_head_lst = ['Serial','Temperature','VDD','Thru']
df_head_lst += ['IL @ ' + el for el in list(freq_dict.keys())]
df_head_lst += ['ISO @ ' + el for el in list(freq_dict.keys())]
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
    print('\r{}% Complete: {}/{}'.format(c,a,b))

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
            if 'ANT1' in d['Thru']:
                d[ele] = tmpobj[1,states2il_dict[d['Thru']]][tmp2[2]].s_db[0,0,0]
            else:
                d[ele] = tmpobj[2,states2il_dict[d['Thru']]][tmp2[2]].s_db[0,0,0]
        elif (tmp2[0]=='ISO'):
            d[ele] = np.max([tmpobj[band][tmp2[2]].s_db[0,0,0] for band in states2iso_dict[d['Thru']]])
        else:
            if 'ANT1' in d['Thru']:
                d[ele] = tmpobj[1,1][tmp2[2]].s_db[0,0,0]
            else:
                d[ele] = tmpobj[2,2][tmp2[2]].s_db[0,0,0]
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






