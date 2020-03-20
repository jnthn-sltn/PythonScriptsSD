# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 16:25:46 2020

@author: joslaton
"""
#%%
import skrf as rf
import matplotlib
rf.stylely()
from pylab import *

# load data for the waveguide to CPW probe
probe = rf.Network(r"\\malibu\benchdata\1_Engineers\joslaton\Deembedding_Files\SCOOBY\SCOOBY_DEEMBED2_BOOGALOO.s2p")

# %%
# we will focus on s11
s11 = probe.s11

#  time-gate the first largest reflection
s11_gated = s11.time_gate(center=0.1182, span=0.2364)
s11_gated.name='gated probe'

# plot frequency and time-domain s-parameters
figure(figsize=(8,4))
subplot(121)
s11.plot_s_db()
s11_gated.plot_s_db()
title('Frequency Domain')

subplot(122)
s11.plot_s_db_time()
s11_gated.plot_s_db_time()
title('Time Domain')
tight_layout()

# %% 
# we will focus on s21
s21 = probe.s21

#  time-gate the first largest reflection
s21_gated = s21.time_gate(center=0.23, span=.44)
s21_gated.name='gated probe'

# plot frequency and time-domain s-parameters
figure(figsize=(8,4))
subplot(121)
s21.plot_s_db()
s21_gated.plot_s_db()
title('Frequency Domain')

subplot(122)
s21.plot_s_db_time()
s21_gated.plot_s_db_time()
title('Time Domain')
tight_layout()

# %%
T11 = probe.t11