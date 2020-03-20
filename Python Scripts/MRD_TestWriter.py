# -*- coding: utf-8 -*-
"""
Created on Tue Feb 25 10:21:34 2020.

@author: joslaton
"""

# %% Imports
from psvmodule import get_commands, get_register_df, save_commands, save_mrd
# %% User Input Allowed 1

# MMC NOTE
# prd_file is the excel file where the register maps can be found
prd_file = r"\\malibu\benchdata\1_Engineers\joslaton\METEOR\Meteor Reg Map PRD.xlsx"
# MMC NOTE
# prd_sheet_stand_reg is the name of the sheet in the excel file
# where the standard register map can be found.
prd_sheet = 'USID8'
# MMC NOTE
# prd_sheet_ext_reg is the name of the sheet in the excel file
# where the extended register map can be found.
prd_sheet_extended = 'Extended'

# %% User Input Allowed 2

# The format for mtrig_dict is seen below.
# The 'Reg' field is filled with the hex address of the
# register that controls the trigger mapping.
# The U/L field is filled with the location of the bits
# that control the trigger mapping. In the example seen below,
# Mappable trigger group A (MA) and Mappable trigger group B (MB) are both
# controlled by Reg0x11. The upper four bits of Reg0x11 ([7:4]) controls
# MB. The lower four bits of Reg0x11 ([3:0]) controls MA.
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
# MMC NOTE
# out_stand_file is the excel file where the machine readable
# standard register map will be output. Must be a CSV.
mrd_file = prd_file.split('.')[0] + "_MRD.csv"
# output_file is the path for the output. NO INPUT NEEDED.
test_output_file = '\\'.join(prd_file.split('\\')[:-1]) + '\\TSEQ.csv'

# %%
# Get list of Registers
register_df, usid = get_register_df(prd_file, prd_sheet, prd_sheet_extended)

# %% Print MRD to CSV
save_mrd(register_df, mrd_file)


# %%
command_list = get_commands(register_df, mtrig_dict, usid)

# %%
save_commands(command_list, test_output_file)
