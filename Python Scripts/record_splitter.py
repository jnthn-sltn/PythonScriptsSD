# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 17:59:50 2019

@author: jonslaton
"""

def strip_header(s):
    return s.split(',')[1].strip()

class csv_record:
    def __init__(self,rec):
        self.test_system = strip_header(rec[0])
        self.setup_file = strip_header(rec[1])
        self.cal_dir = strip_header(rec[2])
        self.part_num = strip_header(rec[3])
        self.operator = strip_header(rec[4])
        self.station = strip_header(rec[5])
        self.date_of_record = strip_header(rec[6])
        self.start_time = ''.join(strip_header(rec[7]).split(':'))
        self.col_header = rec[8].strip('\n')
        self.result = rec[9:-1]
        self.name = '--'.join([self.part_num] + self.result[0].split(',')[0:3] + [self.start_time])
        
    def print_to_file(self,fdir):
        import pathlib
        pathlib.Path(fdir + 'Splits').mkdir(exist_ok=True)
        with open( fdir + 'Splits/' + self.name + '.csv' ,'w') as f:
            f.write(self.col_header + '\n')
            f.writelines(self.result)
        
            
        

#brief:     A utility function to read csv's into memory.
#param:  fname  A string path to the csv to be read.   
#return:    a   A list containing all lines of the csv.
def read_test_csv(fname):
    a = []
    with open(fname,'r') as f:
        for line in f.readlines():
            a += [line]
    return a

def split_records(all_records):
    a = []
    b = []
    i = 0
    start_pos = []
    while i < len(all_records):
        if (all_records[i][0] == '#'):
            start_pos += [i]
            i+=8
        i+=1
    i=0
    while ( (i+1) < len(start_pos) ):
        a += [all_records[start_pos[i]:start_pos[i+1]]]
        i+=1
    a += [all_records[start_pos[i]:-1]]
    for record in a:
        b += [csv_record(record)]
    return b