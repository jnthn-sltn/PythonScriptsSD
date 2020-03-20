# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 10:06:40 2020.

@author: joslaton
"""


import skrf as rf
import os
import pathlib

# %% 1


def filename_collector(fdir):
    a = []
    for root, dirs, files in os.walk(fdir):
        for filename in files:
            a += [root + '\\' + filename]
    return a


def file_renamer(fdir):
    a = []
    for fname in fdir:
        tmp = fname.split('\\')
        tmp[-5] = tmp[-5] + '_Deembedded'
        a += ['\\'.join(tmp)]
    return a


def file_mapper(flist_dst):
    dir_lst = list(set(['\\'.join(el.split('\\')[:-1]) for el in flist_dst]))
    for el in dir_lst:
        pathlib.Path(el).mkdir(parents=True, exist_ok=True)


def status_tracker(a, b):
    c = float(a) / b
    print('\r{:.2%} Complete: {}/{}'.format(c, a, b))


def comment_collector(fname, first_line=True):
    a = []
    with open(fname, 'r') as f:
        b = f.readlines()
    a = [line for line in b if line[0] == '!']
    if first_line:
        a = a[:7]
    else:
        a = a[7:]
    return a


def copy_comments(fname1, fname2, first_line=True):
    a = comment_collector(fname1, first_line)
    if first_line:
        with open(fname2, 'w') as f:
            f.writelines(a)
    else:
        with open(fname2, 'a') as f:
            f.writelines(a)

# %% 2
RF1_Path = r"\\malibu\benchdata\1_Engineers\joslaton\Deembedding_Files\SCOOBY\SCOOBY_DEEMBED_TRY2__1.s2p"
RF2_Path = r"\\malibu\benchdata\1_Engineers\joslaton\Deembedding_Files\SCOOBY\SCOOBY_DEEMBED_TRY2__2.s2p" 
DUT_dir = r"C:\Users\joslaton\Documents\S-Params\ES2_DV"

RF1 = rf.Network(RF1_Path)
RF2 = rf.Network(RF2_Path)

# %% 3

flist_src = filename_collector(DUT_dir)
flist_dst = file_renamer(flist_src)

# %% 4
file_mapper(flist_dst)

# %% 5
num_files = len(flist_src)
for i in range(num_files):
    DUT = rf.Network(flist_src[i])
    DUTd = RF1.inv ** DUT ** RF2.inv
    tmp = flist_dst[i].split('\\')
    DUTd_dir = '\\'.join(tmp[:-1])
    DUTd_fname = tmp[-1].split('.')[0]
    DUTd.frequency.unit = 'Hz'
    copy_comments(flist_src[i], flist_dst[i], first_line=True)
    hldr = DUTd.write_touchstone(filename=DUTd_fname, dir=DUTd_dir,
                                  skrf_comment=False, return_string=True,
                                  form='db')
    with open(flist_dst[i], 'a') as f:
        f.writelines(hldr)
    copy_comments(flist_src[i], flist_dst[i], first_line=False)
    status_tracker(i+1, num_files)
