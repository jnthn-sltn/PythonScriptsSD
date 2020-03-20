# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 11:47:12 2019.

@author: joslaton
"""

# %% 1
import pandas as pd


def parse_extended_bits(df):
    len_lst = list(map(lambda x: len(x), df['Default']))
    idx_lst1 = [i for i in range(len(len_lst)) if len_lst[i] < 5]
    df['Default'].iloc[idx_lst1] = list(
        map(lambda x: int(x, 16), df['Default'].iloc[idx_lst1])
        )
    return df

def parse_bits(df):
    # Make a list containing the lengths of the default value strings
    len_lst = list(map(lambda x: len(x), df['Default']))
    idx_lst1 = [i for i in range(len(len_lst)) if len_lst[i] == 1]
    idx_lst2 = [i for i in range(len(len_lst)) if len_lst[i] == 8]
    df['Default'].iloc[idx_lst1] = list(
        map(lambda x: int(x[0], 16), df['Default'].iloc[idx_lst1])
        )
    df['Default'].iloc[idx_lst2] = list(
        map(lambda x: int(''.join(x), 2), df['Default'].iloc[idx_lst2])
        )
    idx_lst3 = [i for i in range(len(len_lst)) if
                len_lst[i] != 1 and len_lst[i] != 8]
    idx_lst4 = [el for el in idx_lst3 if
                'x' not in ''.join(df['Default'].iloc[el])]
    df['Default'].iloc[idx_lst4] = list(
        map(lambda x: int(''.join(x).replace(' ', ''), 2),
            df['Default'].iloc[idx_lst4])
        )
    return df


def concat_bits(idx_lst, df):
    i = 0
    a_lst = []
    while i < (len(idx_lst)-1):
        a_lst = [str(el) for el in df['Default'].iloc[
            idx_lst[i]:idx_lst[i + 1]
            ] if type(el) != bool]
        df['Default'].iloc[idx_lst[i]] = a_lst
        i += 1
    if (df.iloc[-1].name == df.iloc[idx_lst[i]].name):
        a_lst = [str(df['Default'].iloc[-1])]
    else:
        a_lst = [str(el) for el in
                 df['Default'].iloc[idx_lst[i]] if type(el) != bool]
    df['Default'].iloc[idx_lst[i]] = a_lst
    df = df.iloc[idx_lst].reset_index(drop=True)
    return df

def insert_rows(idx, df, df_insert,offset):
    dfA = df.iloc[:idx, ]
    dfB = df.iloc[idx+offset:, ]
    df = dfA.append(df_insert).append(dfB).reset_index(drop=True)
    return df


def df_cleaner(df):
    # Drop NaN rows and reindex.
    df.dropna(axis=0, how='all', inplace=True)
    df = df.reset_index(drop=True)
    # Get the index of the 48-55 registers.
    small_df = df[
        df['Register Address (Dec.)'].str.contains('-').fillna(False)
        ]
    adx = small_df['Register Address (Dec.)'].tolist()
    begin_adx = [int(el.split('-')[0]) for el in adx]
    end_adx = [int(el.split('-')[1]) for el in adx]
    # Create rows to be inserted.
    for i in range(len(adx)):
        span = end_adx[i]-begin_adx[i]+1
        temp_df = pd.DataFrame([small_df.iloc[i]]*span)
        temp_reg_lst = [i for i in range(begin_adx[i], end_adx[i]+1)]
        hex_temp_reg_lst = [hex(i) for i in temp_reg_lst]
        temp_df['Register Address (Dec.)'] = temp_reg_lst
        temp_df['Register Address (Hex.)'] = hex_temp_reg_lst
        smaller_df = df[
            df['Register Address (Dec.)'].str.contains('-').fillna(False)
            ]
        idx_lst = smaller_df.index.tolist()
        df = insert_rows(idx_lst[0], df, temp_df, 1).fillna(False)
    idx_lst2 = df['Implementation Required'].where(
        df['Implementation Required'].astype(bool)
        ).dropna().index.tolist()
    df = concat_bits(idx_lst2, df)
    return df
# %% 2


# MMC NOTE
# prd_sheet_stand_reg is the name of the sheet in the excel file
# where the standard register map can be found.
prd_sheet_stand_reg = 'USID8'
# MMC NOTE
# prd_file is the excel file where the register maps can be found
prd_file = r"\\malibu\benchdata\1_Engineers\joslaton\METEOR\Meteor Reg Map PRD.xlsx"
# MMC NOTE
# prd_sheet_ext_reg is the name of the sheet in the excel file
# where the extended register map can be found.
prd_sheet_ext_reg = 'Extended'
# MMC NOTE
# out_stand_file is the excel file where the machine readable
# standard register map will be output. Must be a CSV.
out_stand_file = r"\\malibu\benchdata\1_Engineers\joslaton\METEOR\Meteor_USID8.csv"
# MMC NOTE
# out_ext_file is the excel file where the machine readable
# extended register map will be output. Must be a CSV.
out_ext_file = r"\\malibu\benchdata\1_Engineers\joslaton\METEOR\Meteor_Extended.csv"

# %% 3
stand_reg_df = pd.read_excel(prd_file,
                             sheet_name=prd_sheet_stand_reg,
                             header=0,
                             usecols=['Implementation Required',
                                      'Register Address (Dec.)',
                                      'Register Address (Hex.)',
                                      'Default',
                                      'Trigger Support',
                                      'Active Trigger',
                                      'Extended Register R/W',
                                      'Masked Write Support',
                                      'R/W'])

# %% 4
stand_reg_df = df_cleaner(stand_reg_df)

# %% 5
stand_reg_df = parse_bits(stand_reg_df)
# %% 6
stand_reg_df['Register Address (Dec.)'] = list(
    map(lambda x: int(x, 16), stand_reg_df['Register Address (Hex.)'])
    )
# %% 7

# Print to file
stand_reg_df.to_csv(path_or_buf=out_stand_file, index=False)

# %% 8
'''
EXTENDED REGISTER CLEANING
'''

ext_reg_df = pd.read_excel(prd_file,
                           sheet_name=prd_sheet_ext_reg,
                           header=0,
                           usecols=['Register Address (Hex.)',
                                    'Implementation Required',
                                    'Default',
                                    'Triggered',
                                    'Mask-Write Support'])

# %% 9
ext_reg_df.dropna(axis=0, how='all', inplace=True)
ext_reg_df.reset_index(drop=True)
ext_reg_df['Register Address (Dec.)'] = list(
    map(lambda x: int(x, 16) if len(x) == 4 else x,
        ext_reg_df['Register Address (Hex.)']))
# %% 10
ext_reg_df = df_cleaner(ext_reg_df)
# %% 11
ext_reg_df = parse_bits(ext_reg_df)
# %% 12
col_dict = {'MIPI Address': 'Register Address (Hex.)',
            'Mask-Write Support': 'Masked Write Support',
            'Triggered': 'Trigger Support'}

# %% 13
ext_reg_df = ext_reg_df.rename(index=str, columns=col_dict)
# %% 14
ext_reg_df['Masked Write Support'] = ['Yes' if el == 'Y'
                                      else 'No' for el
                                      in ext_reg_df['Masked Write Support']]
ext_reg_df['Active Trigger'] = [el if el != 'N'
                                else 'N/A' for el
                                in ext_reg_df['Trigger Support']]
ext_reg_df['Trigger Support'] = ['Yes' if el != 'N'
                                 else 'No' for el
                                 in ext_reg_df['Trigger Support']]
ext_reg_df['Extended Register R/W'] = ['Yes' for el in
                                       ext_reg_df['Register Address (Hex.)']]
ext_reg_df['R/W'] = ['R/W' for el in ext_reg_df['Register Address (Hex.)']]

# %% 15
ext_reg_df = ext_reg_df[['Implementation Required',
                         'Register Address (Dec.)',
                         'Register Address (Hex.)',
                         'Default',
                         'Trigger Support',
                         'Active Trigger',
                         'Extended Register R/W',
                         'Masked Write Support',
                         'R/W']]
ext_reg_df['Default'] = ext_reg_df['Default'].astype(int)
# %% 16

ext_reg_df.to_csv(path_or_buf=out_ext_file, index=False)
