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
    
    # define rgba colors
    red = (1, 0, 0, 1)
    green = (0, 1, 0, 1)
    blue = (0, 0, 1, 1)

    p_c_b = make_cmap_from_hex([mid_purple, mid_coral, mid_brightblue])
    plot_cmap_lightness(p_c_b)
    
    multi_color = make_cmap_from_hex(colors)
    plot_cmap_lightness(multi_color)
    
    rgb = make_cmap_from_rgba([red, green, blue])
    plot_cmap_lightness(rgb)
    
