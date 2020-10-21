# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 08:35:34 2020.

@author: joslaton
"""
# %%

from psvmodule import (psv_loadwriter,
                       psv_loadfile,
                       psv_processfile,
                       psv_save_excel)

# %%
# trig_reg_ddict is filled in from the PRD by the user.
# For example, to trigger T0, a write of 0x01 is sent to Reg0x1C.
# In the example below, we see that the format for triggers is
# {'TRIGGER_ADDRESS': {'TRIGGERING VALUE': 'TRIGGER NAME'}}
# Trigger counters do not have a specific triggering value,
# so the format for them is more simple.
# {'TRIGGER COUNTER ADDRESS': 'TRIGGER COUNTER NAME'}
# Mappable triggers are filled in the following way.
# {'MTRIG ADDRESS': {'MASK':'MTRIG NAME'}}
# The 'mtrig' field should not need to be changed.
# trig_reg_ddict = {'0x1C': {'0x01': 'T0',
#                            '0x02': 'T1',
#                            '0x04': 'T2'},
#                   '0x2E': {'0x01': 'T3',
#                            '0x02': 'T4',
#                            '0x04': 'T5',
#                            '0x08': 'T6',
#                            '0x10': 'T7',
#                            '0x20': 'T8',
#                            '0x40': 'T9',
#                            '0x80': 'T10'},
#                   '0x2F': {'0x01': 'T11',
#                            '0x02': 'T12',
#                            '0x04': 'T13',
#                            '0x08': 'T14',
#                            '0x10': 'T15',
#                            '0x20': 'T16',
#                            '0x40': 'T17',
#                            '0x80': 'T18 - Not Implemented'},
#                   '0x31': 'TC11',
#                   '0x32': 'TC12',
#                   '0x33': 'TC13',
#                   '0x34': 'TC14',
#                   '0x35': 'TC15',
#                   '0x36': 'TC16',
#                   '0x37': 'TC17',
#                   '0x38': 'TC3',
#                   '0x39': 'TC4',
#                   '0x3A': 'TC5',
#                   '0x3B': 'TC6',
#                   '0x3C': 'TC7',
#                   '0x3D': 'TC8',
#                   '0x3E': 'TC9',
#                   '0x3F': 'TC10',
#                   '0x11': {'0xF0': 'MA',
#                            '0x0F': 'MB'},
#                   '0x12': {'0xF0': 'MC',
#                            '0x0F': 'MD'},
#                   '0x13': {'0xF0': 'ME'},
#                   'mtrig': {'0x00': 'T3',
#                             '0x01': 'T4',
#                             '0x02': 'T5',
#                             '0x03': 'T6',
#                             '0x04': 'T7',
#                             '0x05': 'T8',
#                             '0x06': 'T9',
#                             '0x07': 'T10',
#                             '0x08': 'T11',
#                             '0x09': 'T12',
#                             '0x0A': 'T13',
#                             '0x0B': 'T14',
#                             '0x0C': 'T15',
#                             '0x0D': 'T16',
#                             '0x0E': 'T17',
#                             '0x0F': 'MASKED'}
#                   }
trig_reg_ddict = {'0x1C': {'0x01': 'T0',
                           '0x02': 'T1',
                           '0x04': 'T2'},
                  '0x2E': {'0x01': 'T3',
                           '0x02': 'T4',
                           '0x04': 'T5',
                           '0x08': 'T6',
                           '0x10': 'T7',
                           '0x20': 'T8',
                           '0x40': 'T9',
                           '0x80': 'T10'},
                  '0x2F': {'0x01': 'T11',
                           '0x02': 'T12',
                           '0x04': 'T13',
                           '0x08': 'T14',
                           '0x10': 'T15',
                           '0x20': 'T16',
                           '0x40': 'T17',
                           '0x80': 'T18 - Not Implemented'},
                  '0x31': 'TC11',
                  '0x32': 'TC12',
                  '0x33': 'TC13',
                  '0x34': 'TC14',
                  '0x35': 'TC15',
                  '0x36': 'TC16',
                  '0x37': 'TC17',
                  '0x38': 'TC3',
                  '0x39': 'TC4',
                  '0x3A': 'TC5',
                  '0x3B': 'TC6',
                  '0x3C': 'TC7',
                  '0x3D': 'TC8',
                  '0x3E': 'TC9',
                  '0x3F': 'TC10',
                  '0x11': {'0xF0': 'MA',
                           '0x0F': 'MB'},
                  '0x12': {'0xF0': 'MC',
                           '0x0F': 'MD'},
                  '0x13': {'0xF0': 'ME'},
                  'mtrig': {'0x00': 'T3',
                            '0x01': 'T4',
                            '0x02': 'T5',
                            '0x03': 'T6',
                            '0x04': 'T7',
                            '0x05': 'T8',
                            '0x06': 'T9',
                            '0x07': 'T10',
                            '0x08': 'T11',
                            '0x09': 'T12',
                            '0x0A': 'T13',
                            '0x0B': 'T14',
                            '0x0C': 'T15',
                            '0x0D': 'T16',
                            '0x0E': 'T17',
                            '0x0F': 'MASKED'}
                  }

# %%
rsa_file = r"****.csv"
mrd_file = r"****.csv"
result_input = r"****.csv"

# %%
output_seed = result_input.split('.')[0]
output_path = output_seed + ' Report.xlsx'
src_template_path = "****/Templates/" + \
    "TEMPLATE_Post-Silicon Verification.xlsx"

# %%
writer = psv_loadwriter(src_template_path, output_path)

# %%
result_df = psv_loadfile(result_input)

# %%
psv_processfile(result_df, writer, trig_reg_ddict, rsa_file, mrd_file)


# %%
psv_save_excel(writer, output_path)
