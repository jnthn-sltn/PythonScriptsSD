# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 13:32:46 2019

@author: joslaton
"""

def portable_gui(text1,text2):
    import PySimpleGUI as sg      
    layout = [[sg.Text(text1)],    
                 [sg.InputText(), sg.FileBrowse()],      
                 [sg.Submit(), sg.Cancel()]]      
    window = sg.Window(text2).Layout(layout )
    (event, (source_filename,)) = window.Read()  
    window.Close()
    
    return (event,source_filename)


t1 = 'SHA-1 and SHA-256 Hashes for the file'
t2 = 'SHA-1 & 256 Hash'
(evt,src_fname) = portable_gui(t1,t2)

print(evt, src_fname)    