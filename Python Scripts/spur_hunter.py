# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:54:59 2019

@author: joslaton
"""

import visa

rm = visa.ResourceManager('C:\\windows\\system32\\visa64.dll')

#filt = rm.open_resource(list(rm.list_resources())[0])

sa = rm.open_resource(list(rm.list_resources())[0])

sa.timeout = 65000
sa_freq_write_list = ['FREQ:CENT ' + str(i) + ' MHz' for i in range(1475,2025,5)]
filt_freq_write_list = ['F' + str(i) if i>1500000 else 'F1500000' for i in range(1475000,2025000,5000)]
msrmt_lst = []

try:
    for i in range(len(sa_freq_write_list)):
        #filt.query(filt_freq_write_list[i])
        sa.write(sa_freq_write_list[i])
        msrmt_lst += [sa.query('READ:SAN?')]
        print(str(int(float(msrmt_lst[-1].split(',')[1000]))/1000000) + ' MHz completed.')
finally:
    with open('mipi_spur_hunter_output_empty_board.txt','w') as f:
        f.writelines(el +'\n' for el in msrmt_lst)
