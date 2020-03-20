# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 10:28:46 2020.

@author: joslaton
"""
# %% Constant and Utility Function declaration
# MIPI SPEC DEPENDENT Register Mapping
import pandas as pd
from psvmodule import get_commands, save_commands


# %%
# MMC NOTE
# We should specify our input files below. USER INPUT GOES HERE.
in_file = r"\\malibu\benchdata\1_Engineers\joslaton\METEOR\Meteor Reg Map PRD_MRD.csv"
# MMC NOTE
# usid sets the USID used during testing. USER INPUT GOES HERE.
usid = 8
# MMC NOTE
# output_file is the path for the output. NO INPUT NEEDED.
output_file = '\\'.join(in_file.split('\\')[:-1]) + '\\tseq.csv'

# The format for mtrig_dict is seen below.
#
# mtrig_dict = {
#     'MA': {'Reg': '0x11',
#            'U/L': 'L'},
#     'MB': {'Reg': '0x11',
#            'U/L': 'U'},
#     'MC': {'Reg': '0x12',
#            'U/L': 'L'},
#     'MD': {'Reg': '0x12',
#            'U/L': 'U'},
#     'ME': {'Reg': '0x13',
#            'U/L': 'L'}
#     }

# Change as necessary to reflect the DUT.
mtrig_dict = {
    'MA': {'Reg': '0x11',
           'U/L': 'L'},
    'MB': {'Reg': '0x11',
           'U/L': 'U'},
    'MC': {'Reg': '0x12',
           'U/L': 'L'},
    'MD': {'Reg': '0x12',
           'U/L': 'U'},
    'ME': {'Reg': '0x13',
           'U/L': 'L'}
    }


# %%
reg_df = pd.read_csv(in_file)

# %%
command_list = get_commands(reg_df, mtrig_dict, usid)

# %%
save_commands(command_list, output_file)
