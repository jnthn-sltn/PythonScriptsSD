# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 14:05:34 2019

@author: joslaton
"""

import skrf as rf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def filename_collector(fdir):
    a = []
    for root, _, files in os.walk(fdir):  
        for filename in files:
            a += [root + '\\' +filename]
    return a


input_directory = r"****"

input_list = filename_collector(input_directory)

for el in input_list:
    rf.Network(el).write_spreadsheet()
