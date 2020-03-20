# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 14:33:31 2019.

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
    flist_dst = []
    for fname in flist_src:
        temperature = fname.split('\\')[-3]
        tmp = fname.split('\\')[-1].split('_')
        [voltage, ftp] = tmp[-1].split('.')
        serial = 0
        for i in range(len(tmp)):
            if 'SN' in tmp[i]:
                serial = i
        state = '_'.join(tmp[:serial])
        lot = '_'.join(tmp[serial+1:-1])
        serial = tmp[serial]
        tmp = fdir + '\\' + lot + '\\' + state + '\\' + temperature + '\\' + voltage + '\\' + serial + '.' + ftp
        flist_dst += [tmp]
    return flist_dst


def filename_reformatter_2(flist_src):
    flist_dst = []
    for fname in flist_src:
        temperature = fname.split('\\')[-3]
        tmp = fname.split('\\')[-1].split('_')
        [voltage, ftp] = tmp[-1].split('.')
        serial = '_'.join(tmp[2:-2])
        state = '_'.join(tmp[0:2])
        lot = 'OCTO_TEST'
        tmp = fdir + '\\' + lot + '\\' + state + '\\' + temperature + '\\' + voltage + '\\' + serial + '.' + ftp
        flist_dst += [tmp]
    return flist_dst


def timestamp_remover(flist_src):
    flist_dst = []
    for fname in flist_src:
        s = fname.split('_')[:-2]
        extension = fname.split('.')[-1]
        flist_dst += ['_'.join(s) + '.' + extension]
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

def file_sep(flist_src):
    flist_dst = []
    for fname in flist_src:
        temperature = fname.split('\\')[-2]
        tmp = fname.split('\\')[-1].split('_')
        [voltage,ftp] = tmp[-1].split('.')
        state = '_'.join(tmp[:5])
        serial = tmp[5]
        lot = tmp[-2]
        tmp = fdir + '\\' + lot + '\\' + state + '\\' + temperature + '\\' + voltage + '\\' + serial + '.' + ftp
        flist_dst += [tmp]
    return flist_dst


def file_mapper(flist_dst):
    dir_lst = list(set(['\\'.join(el.split('\\')[:-1]) for el in flist_dst]))
    for el in dir_lst:
        pathlib.Path(el).mkdir(parents=True, exist_ok=True)


def error_corrector(flist_src):
    return [el.split('.')[0]+'.s4p' for el in flist_src]

# %%

fdir = r"C:\Users\joslaton\Documents\S-Params\ASW_Inp_A2"
flist_src = filename_collector(fdir)

# %%

flist_dst = timestamp_remover(flist_src)
uniqueness_tester(flist_dst)

# %%

filename_renamer(flist_src, flist_dst)

# %%

flist_src = filename_collector(fdir)

# %%

flist_dst = filename_reformatter(flist_src)
uniqueness_tester(flist_dst)
# flist_dst = file_sep(flist_src)

# %%

file_mapper(flist_dst)

# %%
filename_renamer(flist_src, flist_dst)

# %%
# file_copier(flist_src, flist_dst)

