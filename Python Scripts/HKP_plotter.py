# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 10:20:20 2019

@author: joslaton
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer
import pathlib

def file_mapper(flist_dst):
    #dir_lst = list(set(['\\'.join(el.split('\\')[:-1]) for el in flist_dst]))
    for el in flist_dst:
        pathlib.Path(el).mkdir(parents=True, exist_ok=True)



fname = r"\\malibu\benchdata\1_Engineers\joslaton\INU\Char\HKP\HKP.xlsx"
output_path = r"//malibu/benchdata/1_Engineers/joslaton/INU/Char/HKP/ALL/"



spec_val = 35


df = pd.read_excel(fname)
df.columns = [col.replace(' ','') for col in df.columns]
df.drop(axis=0,index=list(np.where(df['COND_TEST']=='IDD_IL_CHECK')[0]),inplace=True)
df.reset_index(drop=True,inplace=True)

lst_keep = ['COND_SERIAL_NUMBER',
            'COND_TEMP_C',
            'COND_VDD_V',
            'COND_LOGIC_STATE',
            'COND_BAND',
            'COND_INPUT_FREQ_MHz',
            'COND_INPUT_PWR_dBm',
            'MEAS_INPUT_PWR_PM_READING_dBm',
            'MEAS_FO_OUTPUT_PWR_AVG_dBm',
            'MEAS_FO_OUTPUT_PWR_PEAK_dBm',
            'MEAS_2FO_OUTPUT_PWR_AVG_dBm',
            'MEAS_2FO_OUTPUT_PWR_PEAK_dBm',
            'MEAS_3FO_OUTPUT_PWR_AVG_dBm',
            'MEAS_3FO_OUTPUT_PWR_PEAK_dBm',]
df.drop(labels=[el for el in df.columns if el not in lst_keep],axis=1,inplace=True)

freqs = df['COND_INPUT_FREQ_MHz'].unique().tolist()
#devices = ['SN3', 'SN4', 'SN5']
devices = df['COND_SERIAL_NUMBER'].unique().tolist()
temperatures =  sorted(df['COND_TEMP_C'].unique().tolist())
vbatts = df['COND_VDD_V'].unique().tolist()
file_mapper([output_path]+[output_path + str(vbatt) for vbatt in vbatts])
states = df['COND_LOGIC_STATE'].unique().tolist()
show_states = [el.split('_')[2]+el.split('_')[4] for el in states]#[el.split('_')[4] for el in states]
show_states = dict(zip(range(1,5),show_states))
states = dict(zip(range(1,5),states))

for vbatt in vbatts:
    sub_vbatt_df = df.loc[df['COND_VDD_V']==vbatt]
    start = timer()
    for freq in freqs:
        fig, axs = plt.subplots(len(states),len(temperatures))
        i=0
        fig.set_size_inches((16,9),forward=False)
        freq_df = sub_vbatt_df.loc[sub_vbatt_df['COND_INPUT_FREQ_MHz']==freq]
        title_string = '2Fo HKP for VBATT='+ str(vbatt) +'V, at Fo=' + str(freq)+'MHz'
        fig.suptitle(title_string)
        for state in states.keys():
            sub_state_df = freq_df.loc[freq_df['COND_LOGIC_STATE']==states[state]]
            j=0
            for temp in temperatures:
                sub_temp_df = sub_state_df.loc[sub_state_df['COND_TEMP_C']==temp]
                for device in devices:
                    sub_device_df = sub_temp_df.loc[sub_temp_df['COND_SERIAL_NUMBER']==device]
                    x = sub_device_df['COND_INPUT_PWR_dBm'].tolist()
                    y = sub_device_df['MEAS_2FO_OUTPUT_PWR_AVG_dBm'].tolist()
#                    x = df.loc[(df['COND_VDD_V']==vbatt) & 
#                               (df['COND_INPUT_FREQ_MHz']==freq) &
#                               (df['COND_TEMP_C']==temp) &
#                               (df['COND_LOGIC_STATE']==states[state]) &
#                               (df['COND_SERIAL_NUMBER']==device),'COND_INPUT_PWR_dBm'].tolist()
#                    y = df.loc[(df['COND_VDD_V']==vbatt) & 
#                               (df['COND_INPUT_FREQ_MHz']==freq) &
#                               (df['COND_TEMP_C']==temp) &
#                               (df['COND_LOGIC_STATE']==states[state]) &
#                               (df['COND_SERIAL_NUMBER']==device),'MEAS_2FO_OUTPUT_PWR_AVG_dBm'].tolist()
                    #print(device)
                    #print(y[-1])
                    
                    lstyle='-'
                    label=device
                    axs[i,j].plot(x,y,label=label,linestyle=lstyle)
                axs[i,j].set_title(show_states[state] + ' @ ' + str(int(temp)) + 'C',fontsize='small')
                axs[i,j].vlines(35,-90,0,colors='r',linestyles='dotted',label='Spec Line')
                axs[i,j].set_xbound(lower=30,upper=40)
                axs[i,j].set_xlabel('P_in (dBm)',fontsize='x-small')
                axs[i,j].set_ylabel('2Fo P_out (dBm)',fontsize='x-small')
                axs[i,j].set_ybound(lower=-80,upper=-20)
                j+=1
            i+=1
        #axs[0,0].legend()
        plt.subplots_adjust(top=0.94,bottom=0.058,left=0.037,right=0.988,hspace=0.425,wspace=0.2)
        plt.savefig(output_path + str(vbatt) + '\\' + title_string.replace('.','p') + '.jpg')
    end = timer()
    print('Loop1 time')
    print(end - start)    
    plt.close('all')
    start = timer()
    vbatt_df = df.loc[df['COND_VDD_V']==vbatt]
    for freq in freqs:
        fig, axs = plt.subplots(len(states),len(temperatures))
        i=0
        fig.set_size_inches((16,9),forward=False)
        freq_df = vbatt_df.loc[vbatt_df['COND_INPUT_FREQ_MHz']==freq]
        title_string = '3Fo HKP for VBATT='+ str(vbatt) +'V, at Fo=' + str(freq)+'MHz'
        fig.suptitle(title_string)
        for state in states.keys():
            sub_state_df = freq_df.loc[freq_df['COND_LOGIC_STATE']==states[state]]
            j=0
            for temp in temperatures:
                sub_temp_df = sub_state_df.loc[sub_state_df['COND_TEMP_C']==temp]
                for device in devices:
                    sub_device_df = sub_temp_df.loc[sub_temp_df['COND_SERIAL_NUMBER']==device]
                    x = sub_device_df['COND_INPUT_PWR_dBm'].tolist()
                    y = sub_device_df['MEAS_3FO_OUTPUT_PWR_AVG_dBm'].tolist()
                    #print(y)
                    lstyle='-'
                    label=device
                    axs[i,j].plot(x,y,label=label,linestyle=lstyle)
                axs[i,j].set_title(show_states[state] + ' @ ' + str(int(temp)) + 'C',fontsize='small')
                axs[i,j].vlines(35,-90,0,colors='r',linestyles='dotted',label='Spec Line')
                axs[i,j].set_xbound(lower=30,upper=40)
                axs[i,j].set_xlabel('P_in (dBm)',fontsize='x-small')
                axs[i,j].set_ylabel('3Fo P_out (dBm)',fontsize='x-small')
                axs[i,j].set_ybound(lower=-60,upper=-20)
                j+=1
            i+=1
        #axs[0,0].legend()
        plt.subplots_adjust(top=0.94,bottom=0.058,left=0.037,right=0.988,hspace=0.425,wspace=0.2)
        plt.savefig(output_path + str(vbatt) + '\\' + title_string.replace('.','p') + '.jpg')
    end=timer()
    print('Loop2 time')
    print(end - start)
    
    plt.close('all') 
        
        