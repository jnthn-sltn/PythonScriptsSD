# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 15:12:53 2019

@author: joslaton
"""

def find_first_last(a_lst):
    find_last = 0
    first = 0
    last = 0
    tup_lst = []
    i = 0
    while i < len(a_lst):
        if '#' == a_lst[i][0]:
            if not find_last:
                first = i
                find_last = 1
                i += 8
            else:
                last = i
                find_last = 0
                i -= 1
                tup_lst += [(first,last)]
        else:
            i+=1
    last = len(a_lst)-1
    tup_lst += [(first,last)]
    return tup_lst


src_file = r"C:\Users\joslaton\Downloads\Data_*****_char1_*****02_20190911.csv"
out_file_seed = src_file.split('.')[0]

f_lst = []
with open(src_file,'r') as f:
    f_lst += f.readlines()

fl_lst = find_first_last(f_lst)
i=0
last_line = len(fl_lst)
for el in fl_lst:
    i+=1
    if i==1:
        with open(out_file_seed+'_Headerless'+'.csv','w+') as f:
            f.writelines(f_lst[el[0]+8:el[1]])
    elif i==last_line:
        with open(out_file_seed+'_Headerless'+'.csv','a+') as f:
            f.writelines(f_lst[el[0]+9:el[1]+1])
    else:
        with open(out_file_seed+'_Headerless'+'.csv','a+') as f:
            f.writelines(f_lst[el[0]+9:el[1]])