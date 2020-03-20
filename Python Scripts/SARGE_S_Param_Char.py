# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 10:01:55 2019

@author: joslaton
"""

import os
import numpy as np
import skrf as rf
import pandas as pd

input_dir = r"\\malibu\benchdata\1_Engineers\joslaton\SARGE\DV\Dedicated\S-Parameters"

states2il_dict = {'LS_ASW_TRX_1_B26':7,
                  'LS_ASW_TRX_2_B8':8,
                  'LS_ASW_TRX_3_B12':9,
                  'LS_ASW_TRX_4_B29':10,
                  'LS_ASW_TRX_5_TRX2':11,
                  'LS_ASW_TRX_6_TRX1':12,
                  'LS_ASW_TRX_7_B28B':6,
                  'LS_ASW_TRX_8_B20':5,
                  'LS_ASW_TRX_9_B14':4,
                  'LS_ASW_TRX_10_B28A':3,
                  'LS_ASW_TRX_11_B71A':2,
                  'LS_ASW_TRX_12_B71B':13}

rev_states2il_dict = dict(zip(list(states2il_dict.values()),list(states2il_dict.keys())))

states2iso_dict = {'LS_ASW_TRX_1_B26':[(7,i) for i in range(2,14) if i not in [7,8]],
                  'LS_ASW_TRX_2_B8':[(8,i) for i in range(2,14) if i not in [7,8,9]],
                  'LS_ASW_TRX_3_B12':[(9,i) for i in range(2,14) if i not in [8,9,10]],
                  'LS_ASW_TRX_4_B29':[(10,i) for i in range(2,14) if i not in [9,10,11]],
                  'LS_ASW_TRX_5_TRX2':[(11,i) for i in range(2,14) if i not in [10,11,12]],
                  'LS_ASW_TRX_6_TRX1':[(12,i) for i in range(2,14) if i not in [11,12]],
                  'LS_ASW_TRX_7_B28B':[(6,i) for i in range(2,14) if i not in [5,6]],
                  'LS_ASW_TRX_8_B20':[(5,i) for i in range(2,14) if i not in [4,5,6]],
                  'LS_ASW_TRX_9_B14':[(4,i) for i in range(2,14) if i not in [3,4,5]],
                  'LS_ASW_TRX_10_B28A':[(3,i) for i in range(2,14) if i not in [2,3,4]],
                  'LS_ASW_TRX_11_B71A':[(2,i) for i in range(2,14) if i not in [2,3]],
                  'LS_ASW_TRX_12_B71B':[(13,i) for i in range(2,14) if i!=13]}

freq_dict = {'490MHz':1,
          '800MHz':2,
          '960MHz':3}

temperatures = {'-30C':-30,'25C':25,'85C':85}
voltages = {'1p50':1.5,'1p80':1.8,'2p20':2.2}

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
    
    d['Serial'] = tmp[13].split('.')[0]
    d['Temperature'] = temperatures[tmp[11]]
    d['VDD'] = voltages[tmp[12]]
    d['Thru'] = tmp[10]
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

