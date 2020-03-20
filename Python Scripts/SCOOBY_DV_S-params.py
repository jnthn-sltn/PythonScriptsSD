# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:43:06 2020.

@author: joslaton
"""
# 0
import skrf as rf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% 1

p_string = r"C:\Users\joslaton\Documents\S-Params\ES2_DV_Deembedded"
output_path = r"C:\Users\joslaton\Documents\S-Params\Outputs"

states = ['LS_CFG(' + str(k) + ')' for k in range(0, 127, 2) if k in [0,2,4,8,
                                                                      16,32,64,
                                                                      94,126]]

temperatures = ['-40C',
                '25C',
                '105C']
voltages = ['5p50',
            '3p30',
            '2p30']

s_dict = dict(zip(states, range(len(states))))
rev_sdict = dict(zip(range(len(states)), states))
t_dict = dict(zip(temperatures, range(len(temperatures))))
rev_tdict = dict(zip(range(len(temperatures)), temperatures))
v_dict = dict(zip(voltages, range(len(voltages))))
rev_vdict = dict(zip(range(len(voltages)), voltages))

il_dict = {0: 's21'}


serials = ['SN6', 'SN8', 'SN12', 'SN13', 'SN14']

# %% 2

states2il_dict = {'LS_CFG(' + str(k) + ')': (2, 1) for k in range(0, 127, 2)}


states2thru_dict = {'LS_CFG(0)': 'Attenuation: 0 dB',
                    'LS_CFG(2)': 'Attenuation: 0.5 dB',
                    'LS_CFG(4)': 'Attenuation: 1 dB',
                    'LS_CFG(8)': 'Attenuation: 2 dB',
                    'LS_CFG(16)': 'Attenuation: 4 dB',
                    'LS_CFG(32)': 'Attenuation: 8 dB',
                    'LS_CFG(64)': 'Attenuation: 16 dB',
                    'LS_CFG(94)': 'Attenuation: 23.5 dB',
                    'LS_CFG(126)': 'Attenuation: 31.5 dB'}
# %% 3


# %% 4
###############################################################################

class rf_record:
    def __init__(self, state, temperature, voltage, serial):
        self.state = state
        self.temperature = temperature
        self.voltage = voltage
        self.serial = serial
        self.path = p_string + '\\' + state + '\\' + temperature + '\\' + voltage + '\\' + serial + '.s2p'
        self.rfobj = rf.Network(self.path)
        self.row = v_dict[self.voltage]
        self.col = t_dict[self.temperature]
        self.rfobj.frequency.unit = 'ghz'
        self.insertion_loss = states2il_dict[self.state]


###############################################################################
# %% 5
a = []

for state in states:
    for temperature in temperatures:
        for voltage in voltages:
            for serial in serials:
                a += [rf_record(state, temperature, voltage, serial)]
# %% 6
# b = [rec for rec in a if all([rec.serial!='SN1',rec.serial!='SN4'])]
b = [rec for rec in a]

fig_lst = []
ax_lst = []

for state in states:
    fig_t, axes_t = plt.subplots(3, 3)
    fig_t.suptitle(states2thru_dict[state] + ': Return Loss' )
    fig_lst += [fig_t]
    ax_lst += [axes_t]



for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_title('Voltage: ' + rev_vdict[i] + ', Temp: ' + rev_tdict[j])
            

    
# %% 7
#Insertion Loss Plotter
for el in b:
    el.rfobj[1,1].plot_s_db(
        ax=ax_lst[s_dict[el.state]][el.row,el.col],
        label=el.serial+', RL')

# %% 8
for ax in ax_lst:
    for i in range(3):
        for j in range(3):
            ax[i,j].set_ylim(bottom=-45,top=-0.1)
            ax[i,j].legend(loc='lower right',fontsize='xx-small').remove()

for fig in fig_lst:
    fig.set_size_inches((18.81,9.3),forward=False)
    fig.subplots_adjust(top=0.928,bottom=0.061,left=0.041,right=0.99,hspace=0.338,wspace=0.147)
    fig.savefig(output_path +'\\'+ fig.texts[0].get_text().replace(': ',' - ') + '.png')

# %% 9
plt.close(fig='all')

            
# %% 10
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

# %% 11

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