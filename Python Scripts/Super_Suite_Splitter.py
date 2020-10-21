# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 15:03:33 2019.

@author: joslaton
"""

import pandas as pd

src_file = r"****.xlsx"
out_file_seed = src_file.split('.')[0]

src_df = pd.read_excel(src_file, header=0)

uniq_tst_lst = src_df[' COND_TEST'].unique().tolist()

tst_df_dict = {}
for tst in uniq_tst_lst:
    tst_df = src_df.loc[src_df[' COND_TEST'] == tst]
    tst_df_dict[tst] = tst_df.dropna(axis=1, how='all')

for key in list(tst_df_dict.keys()):
    tst_df_dict[key].to_excel(out_file_seed + '_' + key + '.xlsx', index=False)
