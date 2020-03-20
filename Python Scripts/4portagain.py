# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 09:56:04 2019

@author: joslaton
"""

import skrf as rf
from pylab import *
rf.stylely()
import os

def filename_collector(fdir):
    a = []
    for root, dirs, files in os.walk(fdir):  
        for filename in files:
            a += [filename]
    return a

def import_all_networks(fdir):
    