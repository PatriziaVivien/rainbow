#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 11:36:38 2024

@author: patrizia
"""

import matplotlib.pyplot as plt
import numpy as np
from colorspacious import cspace_converter

import matplotlib as mpl
from matplotlib.colors import ListedColormap

def plot_cmap_lightness(cmap):
    x = np.linspace(0.0, 1.0, 100)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(8,5))
    rgb = cmap(x)[np.newaxis, :, :3]

    lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
    Lightnes = lab[0, :, 0]
    L = np.float32(np.vstack((Lightnes, Lightnes, Lightnes)))

    ax.imshow(L, aspect='auto', cmap='binary_r', vmin=0., vmax=100.)
    ax.scatter(x*100, Lightnes/100, c=cmap(x))
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 100)
    ax.set_ylabel('Lightness')
    ax.get_xaxis().set_ticks([])
    plt.show()
    return Lightnes

def sort_rgba_colors_by_lightness(c_list):
    ls = []
    for color in c_list:
        light = get_lightness_from_rgba(mpl.colors.to_rgba(color))
        ls.append(light)
    sorted_index = np.argsort(ls)
    c_sort = np.array(c_list)[sorted_index]
    l_sort = np.array(ls)[sorted_index]
    return c_sort, l_sort
        
def linearise_lightness(c_sort, l_sort):
    #coarse
    l_min = l_sort[0]
    l_max = l_sort[-1]
    l_span = l_max-l_min
    perc_light = [int(((l-l_min)/l_span).round(2)*200) for l in l_sort]
    color_list = []
    ones = np.array([1,1,1,1])
    for i in range(len(perc_light)-1):
        seg_len = perc_light[i+1]-perc_light[i]
        c1 = c_sort[i]
        c2 = c_sort[i+1]
        for j in range(seg_len+1):
            perc_c2 = j/seg_len
            perc_c1 = 1-perc_c2
            col = perc_c1*c1 + perc_c2*c2
            color_list.append(col)
    for i in range(len(color_list)-1):
        while get_lightness_from_rgba(color_list[i])>get_lightness_from_rgba(color_list[i+1]):
            missing_to_white = ones-color_list[i+1]
            color_list[i+1]+=missing_to_white/1000
    #fine
    l_sort = [get_lightness_from_rgba(c) for c in color_list]
    c_sort = color_list
    l_min = l_sort[0]
    l_max = l_sort[-1]
    l_span = l_max-l_min
    perc_light = [int(((l-l_min)/l_span).round(2)*1000) for l in l_sort]
    color_list = []
    ones = np.array([1,1,1,1])
    for i in range(len(perc_light)-1):
        seg_len = perc_light[i+1]-perc_light[i]
        c1 = c_sort[i]
        c2 = c_sort[i+1]
        for j in range(seg_len+1):
            if seg_len==0:
                color_list.append(c1)
                continue
            perc_c2 = j/seg_len
            perc_c1 = 1-perc_c2
            col = perc_c1*c1 + perc_c2*c2
            color_list.append(col)
    return color_list

def make_cmap_from_hex(list_of_hex):
    colors = [mpl.colors.to_rgba(i) for i in list_of_hex]
    cmap = make_cmap_from_rgba(colors)
    return cmap

def make_cmap_from_rgba(list_of_rgba):
    list_of_rgba, list_of_light = sort_rgba_colors_by_lightness(list_of_rgba)
    color_list = linearise_lightness(list_of_rgba, list_of_light)
    cmap = ListedColormap(color_list)
    return cmap

def get_lightness_from_rgba(rgba):
    rgb = rgba[:3]
    lab = cspace_converter("sRGB1", "CAM02-UCS")(rgb)
    Lightnes = lab[0]
    return Lightnes

def combine_cmaps(cmap1, cmap2, cut1_1=0, cut1_2=200, cut2_1=0, cut2_2=200,
                  steps1=200, steps2=200):
    colors = np.vstack((cmap1(np.linspace(0,1,steps1))[cut1_1:cut1_2],
                        
                        cmap2.reversed()(np.linspace(0,1,steps2))[cut2_1:cut2_2]))
    cmap = ListedColormap(colors)
    return cmap
    
reds = []
yellows = []
pinks = []
greens = []
blues = []
oranges = []
nightblues = []
bluegreens = []
grassgreens = []
coppers = []
coldgreens = []
turqoises = []
lavenders = []
deeppinks = []
fire = []
tests = []
max_value = 0.95
max_colors = 10
max_main = [1, 1, 1, 1, 0.96, 0.93, 0.9, 0.8, 0.7, 0.65]
j = np.linspace(1, 2, max_colors)
j_high = np.linspace(1, 1.5, max_colors)
for en, i in enumerate(np.linspace(1,2.5,max_colors)):
    i = (np.exp(i)*1/np.exp(1))
    reds.append((max_main[en], max_value/i, max_value/i, 1))
    yellows.append((max_main[en], max_value/j_high[en], max_value/i, 1))
    pinks.append((max_main[en], max_value/i, max_value/j[en], 1))
    oranges.append((max_main[en], max_value/j[en], max_value/i, 1))
    blues.append((max_value/i, max_value/j[en], max_main[en], 1))
    nightblues.append((max_value/i, max_value/i, max_main[en]/j_high[en], 1))
    bluegreens.append((max_value/i, max_value/j_high[en], max_main[en], 1))
    
    greens.append((max_value/i, max_main[en]/j_high[en], max_value/i, 1))
    grassgreens.append((max_value/j[en], max_main[en]/j_high[en], max_value/i, 1))
    coppers.append((max_main[en]/j_high[en], max_value/j[en], max_value/i, 1))
    coldgreens.append((max_value/i, max_main[en]/j_high[en], max_value/j[en], 1))
    turqoises.append((max_value/i, max_main[en]/j_high[en], max_main[en]/j_high[en], 1))
    lavenders.append((max_value/j[en], max_value/i, max_main[en]/j_high[en], 1))
    deeppinks.append((max_main[en]/j_high[en], max_value/i, max_main[en]/j[en], 1))
    
    fire.append((max_main[en]**2, max_value/i, max_value/(i*2), 1))
    #tests.append((max_value, max_value/j_high[en], max_main[en], 1))

col_list = [coppers, yellows, oranges, 
            reds, pinks, 
            deeppinks, lavenders, 
            nightblues, blues, 
            bluegreens, turqoises,
            coldgreens, greens,
            grassgreens,
            #tests,
            fire]
name_list = ["coppers", "yellows", "oranges", 
            "reds", "pinks", 
            "deeppinks", "lavenders", 
            "nightblues", "blues", 
            "bluegreens", "turqoises",
            "coldgreens", "greens",
            "grassgreens", 
            #"tests",
            "fire"]
col_dict = dict(zip(name_list, col_list))

# =============================================================================
# reds = []
# pinks = []
# greens = []
# blues = []
# oranges = []
# purples = []
# brightblues = []
# grassgreens = []
# coppers = []
# coldgreens = []
# turqoises = []
# lavenders = []
# deeppinks = []
# max_value = 0.95
# max_colors = 10
# max_main = [1, 1, 1, 1, 1, 0.95, 0.9, 0.8, 0.7, 0.6]
# j = np.linspace(1, 2, max_colors)
# j_high = np.linspace(1, 1.5, max_colors)
# for en, i in enumerate(np.linspace(1,2.5,max_colors)):
#     i = (np.exp(i)*1/np.exp(1))
#     reds.append((max_main[en], max_value/i, max_value/i, 1))
#     pinks.append((max_main[en], max_value/i, max_value/j[en], 1))
#     oranges.append((max_main[en], max_value/j[en], max_value/i, 1))
#     blues.append((max_value/i, max_value/i, max_main[en], 1))
#     purples.append((max_value/j[en], max_value/i, max_main[en], 1))
#     brightblues.append((max_value/i, max_value/j_high[en], max_main[en], 1))
#     greens.append((max_value/i, max_main[en]/j_high[en], max_value/i, 1))
#     grassgreens.append((max_value/j[en], max_main[en]/j_high[en], max_value/i, 1))
#     coppers.append((max_main[en]/j_high[en], max_value/j[en], max_value/i, 1))
#     coldgreens.append((max_value/i, max_main[en]/j_high[en], max_value/j[en], 1))
#     turqoises.append((max_value/i, max_main[en]/j_high[en], max_main[en]/j_high[en], 1))
#     lavenders.append((max_value/j[en], max_value/i, max_main[en]/j_high[en], 1))
#     deeppinks.append((max_main[en]/j_high[en], max_value/i, max_main[en]/j[en], 1))
# 
# col_list = [coppers, oranges, 
#             reds, pinks, 
#             deeppinks, lavenders, 
#             purples, blues, 
#             brightblues, turqoises,
#             coldgreens, greens,
#             grassgreens]
# name_list = ["coppers", "oranges", 
#             "reds", "pinks", 
#             "deeppinks", "lavenders", 
#             "purples", "blues", 
#             "brightblues", "turqoises",
#             "coldgreens", "greens",
#             "grassgreens"]
# col_dict = dict(zip(name_list, col_list))
# =============================================================================

mpf_colors = col_dict['bluegreens']
temp_colors = col_dict['reds']
snow_colors = col_dict['blues']
div_cmap =  combine_cmaps(make_cmap_from_rgba(col_dict["turqoises"]), 
                          make_cmap_from_rgba(col_dict["pinks"]),
                          cut1_2=195, steps2=195)

div_rd_bu =  combine_cmaps(make_cmap_from_rgba(col_dict["reds"]), 
                          make_cmap_from_rgba(col_dict["blues"]),
                          cut1_1=10, cut1_2=195, cut2_2=200, steps2=185)

div_lav_green =  combine_cmaps(make_cmap_from_rgba(col_dict["coldgreens"]), 
                          make_cmap_from_rgba(col_dict["lavenders"]),
                          cut1_2=180, cut2_2=180, steps1=190)

cmap_list = []
for i in range(14):
    cmap_list.append(make_cmap_from_rgba(col_list[i]).reversed())

cmap_dict = dict(zip(name_list, cmap_list))

if __name__=='__main__':
    
    # define hex colors
    mid_blue = '#7aadff'
    mid_purple = '#7a7aff'
    mid_violett = '#a77aff'
    mid_pink = '#d77aff'
    mid_coral = '#ff7a7f'
    mid_orange = '#ffba7a'
    mid_lightgreen = '#ccff7a'
    mid_coolgreen = '#7aff97'
    mid_turquoise = '#7affd7'
    mid_brightblue = '#7affff'
    
    red_hex = '#ff0000'
    green_hex = '#00ff00'
    blue_hex = '#0000ff'
    
    colors = [mid_blue, 
              mid_purple, 
              mid_violett, 
              mid_pink, 
              mid_coral, 
              mid_orange, 
              mid_lightgreen,
              mid_coolgreen,
              mid_turquoise,
              mid_brightblue]
    

    fig, axis = plt.subplots(1,1, figsize=(4, 7))
    for i in range(14):
        x = [1,2,3,4,5,6,7,8,9,10]
        y = np.array([1,1,1,1,1,1,1,1,1,1])*i
        axis.scatter(x, y, s=300, c=col_list[i], marker='s')
        axis.set_axis_off()
    
    # define rgba colors
    red = (1, 0, 0, 1)
    green = (0, 1, 0, 1)
    blue = (0, 0, 1, 1)
    plt.show()
    
    
    plot_cmap_lightness(div_rd_bu)
    
    
