# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 12:06:57 2019

@author: joslaton
"""

import skrf as rf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#%%       

p_string =r"\\malibu\benchdata\1_Engineers\joslaton\SARGE\CHAR\S-Parameters"
output_path = r"\\malibu\benchdata\1_Engineers\joslaton\SARGE\CHAR\S-Parameters\ALL"

states = ['LS_ASW_TRX_1_B26',
          'LS_ASW_TRX_2_B8',
          'LS_ASW_TRX_3_B12',
          'LS_ASW_TRX_4_B29',
          'LS_ASW_TRX_5_TRX2',
          'LS_ASW_TRX_6_TRX1',
          'LS_ASW_TRX_7_B28B',
          'LS_ASW_TRX_8_B20',
          'LS_ASW_TRX_9_B14',
          'LS_ASW_TRX_10_B28A',
          'LS_ASW_TRX_11_B71A',
          'LS_ASW_TRX_12_B71B']

temperatures = ['-30C',
                '25C',
                '85C']
voltages = ['2p20',
            '1p80',
            '1p50']

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
 

serials = ['SN1','SN2','SN3','SN4','SN5',
           'SN6','SN7','SN8','SN9','SN10',
           'SN11','SN12','SN13','SN14','SN15',
           'SN17','SN18','SN19','SN20',
           'SN21','SN22','SN23','SN24',
           'SN26','SN27','SN28','SN29','SN31']

#%%

states2il_dict = {'LS_ASW_TRX_1_B26':(7,1),
                  'LS_ASW_TRX_2_B8':(8,1),
                  'LS_ASW_TRX_3_B12':(9,1),
                  'LS_ASW_TRX_4_B29':(10,1),
                  'LS_ASW_TRX_5_TRX2':(11,1),
                  'LS_ASW_TRX_6_TRX1':(12,1),
                  'LS_ASW_TRX_7_B28B':(6,1),
                  'LS_ASW_TRX_8_B20':(5,1),
                  'LS_ASW_TRX_9_B14':(4,1),
                  'LS_ASW_TRX_10_B28A':(3,1),
                  'LS_ASW_TRX_11_B71A':(2,1),
                  'LS_ASW_TRX_12_B71B':(13,1)}

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

states2thru_dict={'LS_ASW_TRX_1_B26':'ANT - B26',
                  'LS_ASW_TRX_2_B8':'ANT - B8',
                  'LS_ASW_TRX_3_B12':'ANT - B12',
                  'LS_ASW_TRX_4_B29':'ANT - B29',
                  'LS_ASW_TRX_5_TRX2':'ANT - TRX2',
                  'LS_ASW_TRX_6_TRX1':'ANT - TRX1',
                  'LS_ASW_TRX_7_B28B':'ANT - B28B',
                  'LS_ASW_TRX_8_B20':'ANT - B20',
                  'LS_ASW_TRX_9_B14':'ANT - B14',
                  'LS_ASW_TRX_10_B28A':'ANT - B28A',
                  'LS_ASW_TRX_11_B71A':'ANT - B71A',
                  'LS_ASW_TRX_12_B71B':'ANT - B71B'}
#%%


#%%
###############################################################################

class rf_record:
   def __init__(self,state,temperature,voltage,serial):
        self.state = state
        self.temperature = temperature
        self.voltage = voltage
        self.serial = serial
        self.path = p_string + '\\' + state + '\\' + temperature + '\\' + voltage + '\\' + serial + '.s13p'
        self.rfobj = rf.Network(self.path)
        self.row = v_dict[self.voltage]
        self.col = t_dict[self.temperature]
        self.rfobj.frequency.unit='ghz'
        self.insertion_loss = states2il_dict[self.state]
        self.iso = states2iso_dict[self.state]
        if 'CA' in self.state:
            port_dict = {3:'B28A',
                         4:'B14',
                         5:'B20',
                         6:'B28B',
                         7:'B26',
                         8:'B8',
                         9:'B12',
                         10:'B29'}
            self.band1=port_dict[self.insertion_loss[0][0]]
            self.band2=port_dict[self.insertion_loss[1][0]]
            
        


###############################################################################
#%%
a = []

for state in states:
    for temperature in temperatures:
        for voltage in voltages:
            for serial in serials:
                a += [rf_record(state,temperature,voltage,serial)]
#%%
#b = [rec for rec in a if all([rec.serial!='SN1',rec.serial!='SN4'])]
b = [rec for rec in a]

fig_lst = []
ax_lst = []

for state in states:
    fig_t, axes_t = plt.subplots(3, 3)
    fig_t.suptitle(states2thru_dict[state] + ': Insertion Loss' )
    fig_lst += [fig_t]
    ax_lst += [axes_t]

#fig_0, axes_0 = plt.subplots(3, 3)
#fig_1, axes_1 = plt.subplots(3, 3)
#fig_2, axes_2 = plt.subplots(3, 3)
#fig_3, axes_3 = plt.subplots(3, 3)
#
#fig_0.suptitle('IN1_OUT1: Insertion Loss')
#fig_1.suptitle('IN2_OUT1: Insertion Loss')
#fig_2.suptitle('IN1_OUT2: Insertion Loss')
#fig_3.suptitle('IN2_OUT2: Insertion Loss')
#
#fig_lst = [fig_0,fig_1,fig_2,fig_3]
#
#ax_lst = [axes_0,axes_1,axes_2,axes_3]

for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_title('Voltage: ' + rev_vdict[i] + ', Temp: ' + rev_tdict[j])
            ax[i,j].plot(range(10000000,1100000000,5000000),[-0.3]*218,'r',label='Typical Spec_Line')
            #ax[i,j].set_ylim(bottom=-1.2,top=0.0)

    
#%%
#Insertion Loss Plotter
for el in b:
    if 'CA' not in el.state:
        el.rfobj[el.insertion_loss]['0.01-1.1ghz'].plot_s_db(ax=ax_lst[s_dict[el.state]][el.row,el.col],label=el.serial+', IL')
    else:
        el.rfobj[el.insertion_loss[0]]['0.01-1.1ghz'].plot_s_db(ax=ax_lst[s_dict[el.state]][el.row,el.col],label=el.serial+', '+ el.band1+', IL')
        el.rfobj[el.insertion_loss[1]]['0.01-1.1ghz'].plot_s_db(ax=ax_lst[s_dict[el.state]][el.row,el.col],label=el.serial+', '+ el.band2+', IL')
#%%
for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_ylim(bottom=-0.7,top=-0.1)
            ax[i,j].legend(loc='lower right',fontsize='xx-small').remove()

for fig in fig_lst:
    fig.set_size_inches((18.81,9.3),forward=False)
    fig.subplots_adjust(top=0.928,bottom=0.061,left=0.041,right=0.99,hspace=0.338,wspace=0.147)
    fig.savefig(output_path +'\\'+ fig.texts[0].get_text().replace(': ',' - ') + '.jpg')

#%%
plt.close(fig='all')

            
#%%
#b = [rec for rec in a if all([rec.serial!='SN1',rec.serial!='SN4'])]
b = [rec for rec in a if rec.state=='LS_ASW_TRX_12_B71B']
#b = [rec for rec in a] ##sooooo sloowww

fig_lst = []
ax_lst = []

for state in states:
    fig_t, axes_t = plt.subplots(3, 3)
    fig_t.suptitle(states2thru_dict[state] + ': Isolation' )
    fig_lst += [fig_t]
    ax_lst += [axes_t]

#fig_0, axes_0 = plt.subplots(3, 3)
#fig_1, axes_1 = plt.subplots(3, 3)
#fig_2, axes_2 = plt.subplots(3, 3)
#fig_3, axes_3 = plt.subplots(3, 3)
#
#fig_0.suptitle('IN1_OUT1: Iso')
#fig_1.suptitle('IN2_OUT1: Iso')
#fig_2.suptitle('IN1_OUT2: Iso')
#fig_3.suptitle('IN2_OUT2: Iso')
#
#fig_lst = [fig_0,fig_1,fig_2,fig_3]
#
#ax_lst = [axes_0,axes_1,axes_2,axes_3]

for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_title('Voltage: ' + rev_vdict[i] + ', Temp: ' + rev_tdict[j])
            ax[i,j].plot(range(10000000,1100000000,5000000),[-30]*218,linestyle=':',color='r',label='WC Spec_Line_30dB')
            ax[i,j].plot(range(10000000,1100000000,5000000),[-33]*218,linestyle=':',color='r',label='Typ Spec_Line_33dB')
            #ax[i,j].set_ylim(bottom=-1.2,top=-0.3)

#%%

for el in b:
    for band in el.iso:
        el.rfobj[band]['0.01-1.1ghz'].plot_s_db(ax=ax_lst[s_dict[el.state]][el.row,el.col],label=el.serial+', IL')
    
print('\a')    
    


#%%
for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_ylim(bottom=-70,top=-20)
            ax[i,j].legend(loc='lower right',fontsize='xx-small').remove()
#%%
for fig in fig_lst:
    fig.set_size_inches((18.81,9.3),forward=False)
    fig.subplots_adjust(top=0.928,bottom=0.061,left=0.041,right=0.99,hspace=0.338,wspace=0.147)
    fig.savefig(output_path +'\\'+ fig.texts[0].get_text().replace(': ',' - ') + '.jpg')

#%%
plt.close(fig='all')
#%%

nominal = [rec for rec in a if all([rec.temperature==rev_tdict[1],rec.voltage==rev_vdict[1]])]
wc = [rec for rec in a if all([rec.temperature==rev_tdict[2],rec.voltage==rev_vdict[0]])]

#%%
states_short = [state for state in states if 'CA' not in state]

#%%
nom_ary = np.zeros([len(states_short),6])
wc_ary = np.zeros([len(states_short),6])

nom_ave_dict = {state:rf.average([rec.rfobj for rec in nominal if (rec.state==state)]) for state in states_short}

wc_ave_dict = {state:rf.average([rec.rfobj for rec in nominal if (rec.state==state)]) for state in states_short}

#%%
line_lst = ['State,IL_490,IL_800,IL_960,'+
            'ISO_490,ISO_800,ISO_960,'+
            'ISO_WCNom_490,ISO_WCNom_800,ISO_WCNom_960,'+
            'WC_IL_490,WC_IL_800,WC_IL_960,'+
            'WC_ISO_490,WC_ISO_800,WC_ISO_960,\n']
for state in states_short:
    nom = nom_ave_dict[state]
    wc = wc_ave_dict[state]
    il_490 = nom[states2il_dict[state]]['0.49GHz'].s_db[0,0,0]
    il_800  = nom[states2il_dict[state]]['0.8GHz'].s_db[0,0,0]
    il_960  = nom[states2il_dict[state]]['0.96GHz'].s_db[0,0,0]
    iso_typ_490 = np.mean([nom[el]['0.49GHz'].s_db[0,0,0] for el in states2iso_dict[state]])
    iso_typ_800 = np.mean([nom[el]['0.8GHz'].s_db[0,0,0] for el in states2iso_dict[state]])
    iso_typ_960 = np.mean([nom[el]['0.96GHz'].s_db[0,0,0] for el in states2iso_dict[state]])
    iso_WCNom_490 = np.max([nom[el]['0.49GHz'].s_db[0,0,0] for el in states2iso_dict[state]])
    iso_WCNom_800 = np.max([nom[el]['0.8GHz'].s_db[0,0,0] for el in states2iso_dict[state]])
    iso_WCNom_960 = np.max([nom[el]['0.96GHz'].s_db[0,0,0] for el in states2iso_dict[state]])
    wc_il_490 = wc[states2il_dict[state]]['0.49GHz'].s_db[0,0,0]
    wc_il_800 = wc[states2il_dict[state]]['0.8GHz'].s_db[0,0,0]
    wc_il_960 = wc[states2il_dict[state]]['0.96GHz'].s_db[0,0,0]
    wc_iso_490 = np.max([nom[el]['0.49GHz'].s_db[0,0,0] for el in states2iso_dict[state]])
    wc_iso_800 = np.max([nom[el]['0.8GHz'].s_db[0,0,0] for el in states2iso_dict[state]])
    wc_iso_960 = np.max([nom[el]['0.96GHz'].s_db[0,0,0] for el in states2iso_dict[state]])
    line_lst += [state + ',' + str(il_490) + ',' + str(il_800) + ',' + str(il_960) + ',' +
                 str(iso_typ_490) + ',' + str(iso_typ_800) + ',' + str(iso_typ_960) + ',' +
                 str(iso_WCNom_490) + ',' + str(iso_WCNom_800) + ',' + str(iso_WCNom_960) + ',' +
                 str(wc_il_490) + ',' + str(wc_il_800) + ',' + str(wc_il_960) + ',' +
                 str(wc_iso_490) + ',' + str(wc_iso_800) + ',' + str(wc_iso_960) + ','+'\n']
    
#%%
with open(output_path+'\\'+'s-params_summary.csv','w') as f:
        f.writelines(line_lst)





#%%
import pandas as pd
header_lst = ['Serial','State','Temperature','VDD','IL_490','IL_800','IL_960','WNAISO_490','WNAISO_800','WNAISO_960']

df = pd.DataFrame(columns=header_lst)

#%%

for el in a:
    c1 = el.serial
    c2 = el.state
    c3 = el.temperature
    c4 = el.voltage
    c5 = el.rfobj[el.insertion_loss]['490MHz'].s_db[0,0,0]
    c6 = el.rfobj[el.insertion_loss]['800MHz'].s_db[0,0,0]
    c7 = el.rfobj[el.insertion_loss]['960MHz'].s_db[0,0,0]
    c8 = np.max([el.rfobj[band]['490MHz'].s_db[0,0,0] for band in el.iso])
    c9 = np.max([el.rfobj[band]['800MHz'].s_db[0,0,0] for band in el.iso])
    c10 = np.max([el.rfobj[band]['960MHz'].s_db[0,0,0] for band in el.iso])
    df = df.append(dict(zip(header_lst,[c1,c2,c3,c4,c5,c6,c7,c8,c9,c10])), ignore_index=True)




#%%
df.to_excel(output_path+'\\'+'s-params_summary_new.xlsx')