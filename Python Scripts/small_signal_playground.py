# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:36:36 2019

@author: joslaton
"""

import skrf as rf
import numpy as np

de_embed_string = r"\\malibu\Users\rpandya\WOLF\Wolf_20190225"
de_embed_ports = ['TXIN1.s2p','TXIN2.s2p','TXOUT1.s2p','TXOUT2.s2p']
de_embed_paths = [de_embed_string+'\\'+port for port in de_embed_ports]


p_string ='\\\\malibu\\benchdata\\1_Engineers\\joslaton\\WOLF\\WOLF_ES2cpy\\WOLF_Spara\\85C\\'
paths = [p_string]*12
states = ['LS_TX_IN1_TX_OUT1_ZEUS_ES2p1_',
          'LS_TX_IN1_TX_OUT2_ZEUS_ES2p1_',
          'LS_TX_IN2_TX_OUT1_ZEUS_ES2p1_',
          'LS_TX_IN2_TX_OUT2_ZEUS_ES2p1_']
voltage = '_3p02.s4p'
pnums = ['SN3','SN4','SN8','SN9','SN10']

paths = [p_string+state+pnum+voltage for pnum in pnums for state in states]
freq_key = '0.1-2.69ghz'

sn3_1 = rf.Network(paths[0])[freq_key]
sn3_2 = rf.Network(paths[1])[freq_key]
sn3_3 = rf.Network(paths[2])[freq_key]
sn3_4 = rf.Network(paths[3])[freq_key]

sn4_1 = rf.Network(paths[4])[freq_key]
sn4_2 = rf.Network(paths[5])[freq_key]
sn4_3 = rf.Network(paths[6])[freq_key]
sn4_4 = rf.Network(paths[7])[freq_key]

sn8_1 = rf.Network(paths[8])[freq_key]
sn8_2 = rf.Network(paths[9])[freq_key]
sn8_3 = rf.Network(paths[10])[freq_key]
sn8_4 = rf.Network(paths[11])[freq_key]

sn9_1 = rf.Network(paths[12])[freq_key]
sn9_2 = rf.Network(paths[13])[freq_key]
sn9_3 = rf.Network(paths[14])[freq_key]
sn9_4 = rf.Network(paths[15])[freq_key]

sn10_1 = rf.Network(paths[16])[freq_key]
sn10_2 = rf.Network(paths[17])[freq_key]
sn10_3 = rf.Network(paths[18])[freq_key]
sn10_4 = rf.Network(paths[19])[freq_key]

dmbd_in1 = rf.Network(de_embed_paths[0])[freq_key]
dmbd_in2 = rf.Network(de_embed_paths[1])[freq_key]
dmbd_out1 = rf.Network(de_embed_paths[2])[freq_key]
dmbd_out2 = rf.Network(de_embed_paths[3])[freq_key]

dmbd31 = dmbd_in1.s21.s_db[0,0,0] + dmbd_out1.s12.s_db[0,0,0]
dmbd41 = dmbd_in1.s21.s_db[0,0,0] + dmbd_out2.s12.s_db[0,0,0]
dmbd32 = dmbd_in2.s21.s_db[0,0,0] + dmbd_out1.s12.s_db[0,0,0]
dmbd42 = dmbd_in2.s21.s_db[0,0,0] + dmbd_out2.s12.s_db[0,0,0]
dmbd21 = dmbd_in1.s21.s_db[0,0,0] + dmbd_in2.s12.s_db[0,0,0]
dmbd43 = dmbd_out1.s21.s_db[0,0,0] + dmbd_out2.s12.s_db[0,0,0]

havana_1_s31 = np.mean([sn3_1.s31.s_db, sn4_1.s31.s_db]) - dmbd31
havana_1_s41 = np.mean([sn3_1.s41.s_db, sn4_1.s41.s_db]) - dmbd41
havana_1_s32 = np.mean([sn3_1.s32.s_db, sn4_1.s32.s_db]) - dmbd32
havana_1_s42 = np.mean([sn3_1.s42.s_db, sn4_1.s42.s_db]) - dmbd42
havana_1_s21 = np.mean([sn3_1.s21.s_db, sn4_1.s21.s_db]) - dmbd21
havana_1_s43 = np.mean([sn3_1.s43.s_db, sn4_1.s43.s_db]) - dmbd43

havana_2_s31 = np.mean([sn3_2.s31.s_db, sn4_2.s31.s_db]) - dmbd31
havana_2_s41 = np.mean([sn3_2.s41.s_db, sn4_2.s41.s_db]) - dmbd41
havana_2_s32 = np.mean([sn3_2.s32.s_db, sn4_2.s32.s_db]) - dmbd32
havana_2_s42 = np.mean([sn3_2.s42.s_db, sn4_2.s42.s_db]) - dmbd42
havana_2_s21 = np.mean([sn3_2.s21.s_db, sn4_2.s21.s_db]) - dmbd21
havana_2_s43 = np.mean([sn3_2.s43.s_db, sn4_2.s43.s_db]) - dmbd43

havana_3_s31 = np.mean([sn3_3.s31.s_db, sn4_3.s31.s_db]) - dmbd31
havana_3_s41 = np.mean([sn3_3.s41.s_db, sn4_3.s41.s_db]) - dmbd41
havana_3_s32 = np.mean([sn3_3.s32.s_db, sn4_3.s32.s_db]) - dmbd32
havana_3_s42 = np.mean([sn3_3.s42.s_db, sn4_3.s42.s_db]) - dmbd42
havana_3_s21 = np.mean([sn3_3.s21.s_db, sn4_3.s21.s_db]) - dmbd21
havana_3_s43 = np.mean([sn3_3.s43.s_db, sn4_3.s43.s_db]) - dmbd43

havana_4_s31 = np.mean([sn3_4.s31.s_db, sn4_4.s31.s_db]) - dmbd31
havana_4_s41 = np.mean([sn3_4.s41.s_db, sn4_4.s41.s_db]) - dmbd41
havana_4_s32 = np.mean([sn3_4.s32.s_db, sn4_4.s32.s_db]) - dmbd32
havana_4_s42 = np.mean([sn3_4.s42.s_db, sn4_4.s42.s_db]) - dmbd42
havana_4_s21 = np.mean([sn3_4.s21.s_db, sn4_4.s21.s_db]) - dmbd21
havana_4_s43 = np.mean([sn3_4.s43.s_db, sn4_4.s43.s_db]) - dmbd43

zeus_1_s31 = np.mean([sn8_1.s31.s_db, sn9_1.s31.s_db, sn10_1.s31.s_db]) - dmbd31
zeus_1_s41 = np.mean([sn8_1.s41.s_db, sn9_1.s41.s_db, sn10_1.s41.s_db]) - dmbd41
zeus_1_s32 = np.mean([sn8_1.s32.s_db, sn9_1.s32.s_db, sn10_1.s32.s_db]) - dmbd32
zeus_1_s42 = np.mean([sn8_1.s42.s_db, sn9_1.s42.s_db, sn10_1.s42.s_db]) - dmbd42
zeus_1_s21 = np.mean([sn8_1.s21.s_db, sn9_1.s21.s_db, sn10_1.s21.s_db]) - dmbd21
zeus_1_s43 = np.mean([sn8_1.s43.s_db, sn9_1.s43.s_db, sn10_1.s43.s_db]) - dmbd43

zeus_2_s31 = np.mean([sn8_2.s31.s_db, sn9_2.s31.s_db, sn10_2.s31.s_db]) - dmbd31
zeus_2_s41 = np.mean([sn8_2.s41.s_db, sn9_2.s41.s_db, sn10_2.s41.s_db]) - dmbd41
zeus_2_s32 = np.mean([sn8_2.s32.s_db, sn9_2.s32.s_db, sn10_2.s32.s_db]) - dmbd32
zeus_2_s42 = np.mean([sn8_2.s42.s_db, sn9_2.s42.s_db, sn10_2.s42.s_db]) - dmbd42
zeus_2_s21 = np.mean([sn8_2.s21.s_db, sn9_2.s21.s_db, sn10_2.s21.s_db]) - dmbd21
zeus_2_s43 = np.mean([sn8_2.s43.s_db, sn9_2.s43.s_db, sn10_2.s43.s_db]) - dmbd43

zeus_3_s31 = np.mean([sn8_3.s31.s_db, sn9_3.s31.s_db, sn10_3.s31.s_db]) - dmbd31
zeus_3_s41 = np.mean([sn8_3.s41.s_db, sn9_3.s41.s_db, sn10_3.s41.s_db]) - dmbd41
zeus_3_s32 = np.mean([sn8_3.s32.s_db, sn9_3.s32.s_db, sn10_3.s32.s_db]) - dmbd32
zeus_3_s42 = np.mean([sn8_3.s42.s_db, sn9_3.s42.s_db, sn10_3.s42.s_db]) - dmbd42
zeus_3_s21 = np.mean([sn8_3.s21.s_db, sn9_3.s21.s_db, sn10_3.s21.s_db]) - dmbd21
zeus_3_s43 = np.mean([sn8_3.s43.s_db, sn9_3.s43.s_db, sn10_3.s43.s_db]) - dmbd43

zeus_4_s31 = np.mean([sn8_4.s31.s_db, sn9_4.s31.s_db, sn10_4.s31.s_db]) - dmbd31
zeus_4_s41 = np.mean([sn8_4.s41.s_db, sn9_4.s41.s_db, sn10_4.s41.s_db]) - dmbd41
zeus_4_s32 = np.mean([sn8_4.s32.s_db, sn9_4.s32.s_db, sn10_4.s32.s_db]) - dmbd32
zeus_4_s42 = np.mean([sn8_4.s42.s_db, sn9_4.s42.s_db, sn10_4.s42.s_db]) - dmbd42
zeus_4_s21 = np.mean([sn8_4.s21.s_db, sn9_4.s21.s_db, sn10_4.s21.s_db]) - dmbd21
zeus_4_s43 = np.mean([sn8_4.s43.s_db, sn9_4.s43.s_db, sn10_4.s43.s_db]) - dmbd43

res_1 = [zeus_1_s31,havana_1_s31,
         zeus_1_s41,havana_1_s41,
         zeus_1_s32,havana_1_s32,
         zeus_1_s42,havana_1_s42,
         zeus_1_s21,havana_1_s21,
         zeus_1_s43,havana_1_s43]

res_2 = [zeus_2_s31,havana_2_s31,
         zeus_2_s41,havana_2_s41,
         zeus_2_s32,havana_2_s32,
         zeus_2_s42,havana_2_s42,
         zeus_2_s21,havana_2_s21,
         zeus_2_s43,havana_2_s43]

res_3 = [zeus_3_s31,havana_3_s31,
         zeus_3_s41,havana_3_s41,
         zeus_3_s32,havana_3_s32,
         zeus_3_s42,havana_3_s42,
         zeus_3_s21,havana_3_s21,
         zeus_3_s43,havana_3_s43]

res_4 = [zeus_4_s31,havana_4_s31,
         zeus_4_s41,havana_4_s41,
         zeus_4_s32,havana_4_s32,
         zeus_4_s42,havana_4_s42,
         zeus_4_s21,havana_4_s21,
         zeus_4_s43,havana_4_s43]
'''
import csv
with open('result.csv','w') as csvfile:
    spwriter=csv.writer(csvfile)
    spwriter.writerow(res_1)
    spwriter.writerow(res_2)
    spwriter.writerow(res_3)
    spwriter.writerow(res_4)
'''