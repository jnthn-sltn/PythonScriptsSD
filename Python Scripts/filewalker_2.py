# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 15:16:24 2020

@author: joslaton
"""

import os
from shutil import copyfile
import pathlib



def uniqueness_tester(a):
    import collections
    print([item for item, count in
           collections.Counter(a).items() if count > 1])


def filename_collector(fdir):
    a = []
    for root, dirs, files in os.walk(fdir):
        for filename in files:
            a += [root + '\\' + filename]
    return a


def filename_reformatter(flist_src):
    cond_list = ['COND_SERIAL_NUMBER',
                 'COND_LOT_NUMBER',
                 'COND_TEMP_C',
                 'COND_VDD_V',
                 'COND_LOGIC_STATE']
    cond_dict = {}
    
    for fname in flist_src:
        tmp_dict = {}
        with open(fname) as f:
            lines = f.readlines()
        flag = 0
        for i in range(len(lines)):
            if flag:
                if lines[i][0] == '!':
                    break
            else:
                if lines[i][0] != '!':
                    flag = 1
        lines = [line.rstrip('\n').lstrip('! ') for line in lines[i:]]
        tmp_dict = {lin: v for }
    
    return flist_dst




def file_copier(flist_src, flist_dst):
    assert len(flist_src) == len(flist_dst)
    for i in range(len(flist_src)):
        copyfile(flist_src[i], flist_dst[i])


def filename_renamer(flist_src, flist_dst):
    assert len(flist_src) == len(flist_dst)
    for i in range(len(flist_src)):
        os.rename(flist_src[i], flist_dst[i])


def filename_renamer_reverser(flist_src, flist_dst):
    for i in range(len(flist_src)):
        os.rename(flist_dst[i], flist_src[i])


def file_mapper(flist_dst):
    dir_lst = list(set(['\\'.join(el.split('\\')[:-1]) for el in flist_dst]))
    for el in dir_lst:
        pathlib.Path(el).mkdir(parents=True, exist_ok=True)


# %%
fdir = r"C:\Users\joslaton\Documents\Python Scripts\DV"

# %%
flist_src = filename_collector(fdir)

# %%
flist_dst = filename_reformatter(flist_src)