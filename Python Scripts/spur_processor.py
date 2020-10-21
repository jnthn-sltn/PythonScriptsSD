# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:03:02 2019

@author: joslaton
"""
#%%
def status_tracker(a,b):
    c = float(a)/b
    print('\r{:.2%} Complete: {}/{}'.format(c,a,b))

def injected_spur_remover(a,b):
    import numpy as np
    a_vals = list(a.values())
    b_vals = list(b.values())
    a_vals = [float(el) for el in a_vals]
    b_vals = [float(el) for el in b_vals]
    a_keys = list(a.keys())
    danl = np.median(b_vals)
    stddv = np.std(b_vals)
    print(str(stddv))
    thresh = danl+5*stddv
    count = 0
    for el in a_vals:
        if el>(thresh):
            count += 1
    print(str(count))
    print(str(thresh))
    new_a_vals = np.array(a_vals)-np.array(b_vals) + danl*np.ones_like(np.array(a_vals))
    new_a_vals = [str(el) for el in new_a_vals]
    new_a = dict(zip(a_keys,new_a_vals))
    return new_a
    
def processed_reloader(a):
    with open(a,'r') as f:
        kv_list = f.readlines()
    k_list = []
    v_list = []
    for el in kv_list:
        k_list += [el.split(',')[0]]
        v_list += [el.rstrip('\n').split(',')[1]]
    loaded_dict = dict(zip(k_list,v_list))
    return loaded_dict

def sa_reformatter(a):
    with open(a,'r') as f:
        kv_list = f.readlines()
    tmp_list = []
    for i in range(len(kv_list)):
        if (i%2==0):
            tmp_list += [kv_list[i]]
    kv_list = tmp_list
    k_list = []
    v_list = []
    #need to unpack each string, then split, then send even numbers to keys and odd numbers to values
    for line in kv_list:
        line = line.rstrip('\n').split(',')
        for i in range(len(line)):
            if (i%2==0):
                k_list += [int(float(line[i]))]
                
            else:
                v_list += [float(line[i])]
    spur_dict = dict(zip(k_list,v_list))
    return spur_dict

def csv_write_file(a,out):
    import csv
    with open(out,'w',newline='') as f:
        csv.writer(f).writerows(a.items())

#%%
infile = r"****.csv"
outfile = r"****.csv"


#%%

msrmt_dict = sa_reformatter(infile)
csv_write_file(msrmt_dict,outfile)

#%%



#%%
msrmtfile = r"****.csv"
thrufile = r"****.csv"
outfile_2 = r"****.csv"

#%%
msrmt_dict = processed_reloader(msrmtfile)
thru_dict = processed_reloader(thrufile)

#%%

msrmt_dict_out = injected_spur_remover(msrmt_dict,thru_dict)

#%%

csv_write_file(msrmt_dict_out,outfile_2)

#%%
for key,val in msrmt_dict.items():
    if val>-144:
        print(str(key) + '  ' + str(val))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        