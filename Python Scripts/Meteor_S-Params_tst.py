# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 10:45:56 2020

@author: joslaton
"""

import os
import numpy as np
import skrf as rf
import pandas as pd

input_dir = r"C:\Users\joslaton\Documents\S-Params\ASW_Inp_A2\Meteor_V2"

states2il_dict = {'LS_MHB_ASW_B3':3,
                  'LS_MHB_ASW_B7':6,
                  'LS_MHB_ASW_B25':2,
                  'LS_MHB_ASW_B34_B29':4,
                  'LS_MHB_ASW_B40':5,
                  'LS_MHB_ASW_B41':7
                  }

rev_states2il_dict = dict(zip(list(states2il_dict.values()),list(states2il_dict.keys())))

states2iso_dict = {'LS_MHB_ASW_B3':[(3,i) for i in range(2,8) if i not in [3]],
                  'LS_MHB_ASW_B7':[(6,i) for i in range(2,8) if i not in [5,6]],
                  'LS_MHB_ASW_B25':[(2,i) for i in range(2,8) if i not in [2,4]],
                  'LS_MHB_ASW_B34_B29':[(4,i) for i in range(2,8) if i not in [2,4]],
                  'LS_MHB_ASW_B40':[(5,i) for i in range(2,8) if i not in [6,5,7]],
                  'LS_MHB_ASW_B41':[(7,i) for i in range(2,8) if i not in [7,5]]
                  }

freq_dict = {'1880MHz':1,
          '1995MHz':2,
          '2025MHz':3,
          '2400MHz':4,
          '2690MHz':5,
          '2695MHz':6}

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
    
    d['Serial'] = tmp[10].split('.')[0]
    d['Temperature'] = temperatures[tmp[8]]
    d['VDD'] = voltages[tmp[9]]
    d['Thru'] = tmp[7]
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

