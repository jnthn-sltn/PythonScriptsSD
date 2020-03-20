# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 16:01:00 2020

@author: joslaton
"""

import pandas as pd
import numpy as np
import skrf as rf

# %% 1


def status_tracker(a,b):
    c = float(a)/b
    print('\r{:.2%} Complete: {}/{}'.format(c, a, b))


def get_ref(indir, t, v, serial):
    ref_net = get_dut(indir, 'LS_CFG(0)', t, v, serial)
    return ref_net


def get_dut(indir, s, t, v, serial):
    dut_p = '\\'.join([indir, s, t, v, serial]) + '.s2p'
    return rf.Network(dut_p)


def get_il(dut, f):
    return dut[f].s21.s_db[0, 0, 0]


def get_reflect(dut, f, port):
    return dut[port, port][f].s_db[0, 0, 0]


def get_att_db(dut,ref,f):
    dut_il = get_il(dut, f)
    ref_il = get_il(ref, f)
    ref_att = -1 * ref_il
    dut_att = -1 * dut_il
    return dut_att - ref_att


# %% 2

input_path = r"C:\Users\joslaton\Documents\S-Params\ES2_DV_Deembedded"
output_path = r"C:\Users\joslaton\Documents\S-Params\Outputs"

states = {'LS_CFG(' + str(k) + ')': k/4.0 for k in range(2, 127, 2)}

temperatures = {'-40C': -40,
                '25C': 25,
                '105C': 105}
voltages = {'5p50': 5.5,
            '3p30': 3.3,
            '2p30': 2.3}

freq_dict = {str(k) + 'GHz': k for k in range(1, 51)}

df_head_lst = ['Serial', 'Temperature', 'VDD',
               'Nominal Attenuation', 'Frequency', 'IL',
               'Meas. Attenuation', 'S11', 'S22']


serials = ['SN6', 'SN8', 'SN12', 'SN13', 'SN14']
# %% 2
num_rows = 2880 * 50
rows_list = []
d = {}
for serial in serials:
    d['Serial'] = serial
    for temperature in temperatures.keys():
        d['Temperature'] = temperatures[temperature]
        for voltage in voltages.keys():
            d['VDD'] = voltages[voltage]
            ref_net = get_ref(input_path, temperature, voltage, serial)
            for state in states.keys():
                d['Nominal Attenuation'] = states[state]
                dut = get_dut(input_path, state, temperature, voltage, serial)
                for freq in freq_dict.keys():
                    d['Frequency'] = freq_dict[freq]
                    d['IL'] = get_il(dut, freq)
                    d['Meas. Attenuation'] = get_att_db(dut, ref_net, freq)
                    d['S11'] = get_reflect(dut, freq, 1)
                    d['S22'] = get_reflect(dut, freq, 2)
                    rows_list.append(d.copy())
                status_tracker(len(rows_list), num_rows)
                    
# %% 3
df = pd.DataFrame(rows_list)
            
#%%

df.to_excel(input_path + '\\' + 'atten_raw.xlsx',index=False)
