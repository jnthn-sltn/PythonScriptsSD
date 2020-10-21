# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 16:20:13 2020

@author: joslaton
"""

import skrf as rf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# %% 1
RF1_Path = r"****"
RF2_Path = r"****"
DUTpath = r"****"

# %% 2

DUT = rf.Network(DUTpath)
DUT.name = 'DUT'

RF1 = rf.Network(RF1_Path).interpolate(DUT.frequency)
RF2 = rf.Network(RF2_Path).interpolate(DUT.frequency)

DUTd = RF1.inv ** DUT ** RF2.inv
# %% 3
DUTd.name = 'DUTd'
# %% 4

fig, axarr = plt.subplots(2,2, sharex=True, figsize=(10,6))

ax = axarr[0,0]
DUTd.plot_s_db(m=0, n=0, ls='-', ax=ax)
DUT.plot_s_db(m=0, n=0, ax=ax, ls=':', color='0.0')
ax.set_title('Return Loss: RF1')
ax.legend(loc='lower center', ncol=3)
ax.grid(True)

ax = axarr[0,1]
DUTd.plot_s_db(m=1, n=0, ls='-', ax=ax)
DUT.plot_s_db(m=1, n=0, ax=ax, ls=':', color='0.0')
ax.set_title('Insertion Loss')
ax.legend(loc='lower center', ncol=3)
ax.grid(True)

ax = axarr[1,0]
DUTd.plot_s_db(m=1, n=1, ls='-', ax=ax)
DUT.plot_s_db(m=1, n=1, ax=ax, ls=':', color='0.0')
ax.set_title('Return Loss: RF2')
ax.legend(loc='lower center', ncol=3)
ax.grid(True)

ax = axarr[1,1]
DUTd.plot_s_deg(m=1, n=0, ax=ax, ls='-', markevery=25)
DUT.plot_s_deg(m=1, n=0, ax=ax, ls=':', color='0.0')
ax.set_title('Insertion Loss')
ax.legend(loc='lower center', ncol=3)
ax.grid(True)

fig.tight_layout()

