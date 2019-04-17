#!/usr/bin/env python2.7

from __future__ import print_function, division 

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as  clr
import h5py 
import pandas as pd

import dtk

def load_catalog(output_fname):
    hfile = h5py.File(output_fname, 'r')
    cat = {}
    for key in hfile:
        cat[key] = hfile[key].value
        print(cat[key])
    return cat

if __name__ == "__main__":
    param = dtk.Param(sys.argv[1])
    input_fname = param.get_string("input_fname")
    output_fname = param.get_string("output_fname")
    steps = param.get_int_list("steps")
    for step in steps:
        print(step)
        cat = load_catalog(output_fname.replace("${step}", str(step)))
        slct_cen = cat['infall_step'] == step
        slct_sat = ~slct_cen
        fig, axs = plt.subplots(2,3, figsize=(20,12))
        
        axs[0,0].set_title("All")
        axs[0,2].set_title("Satellites")
        axs[0,1].set_title('Centrals')
        axs[0,0].set_xlabel('M_infall');
        axs[0,1].set_xlabel('M_infall');
        axs[0,2].set_xlabel('M_infall');
        axs[0,0].set_ylabel("M_peak")
        axs[1,0].set_xlabel("M_peak/M_infall")
        axs[1,1].set_xlabel("M_peak/M_infall")
        axs[1,2].set_xlabel("M_peak/M_infall")

        axs[0,0].hist2d(np.log10(cat['m_infall']), np.log10(cat['m_peak']), bins=100, cmap='Blues', norm=clr.LogNorm())
        axs[0,1].hist2d(np.log10(cat['m_infall'][slct_cen]), np.log10(cat['m_peak'][slct_cen]), bins=100, cmap='Blues', norm=clr.LogNorm())
        axs[0,2].hist2d(np.log10(cat['m_infall'][slct_sat]), np.log10(cat['m_peak'][slct_sat]), bins=100, cmap='Blues', norm=clr.LogNorm())
        axs[1,0].hist(np.log10(cat['m_peak']/cat['m_infall']), bins=100)
        axs[1,1].hist(np.log10(cat['m_peak'][slct_cen]/cat['m_infall'][slct_cen]), bins=100)
        axs[1,2].hist(np.log10(cat['m_peak'][slct_sat]/cat['m_infall'][slct_sat]), bins=100)

        
        plt.tight_layout()

        fig, axs = plt.subplots(2,3, figsize=(20,12))
        axs[0,0].set_title("All")
        axs[0,1].set_title('Centrals')
        axs[0,2].set_title("Satellites")
        axs[0,0].set_ylabel("R_peak")
        axs[0,0].set_xlabel('R_now');
        axs[0,1].set_xlabel('R_now');
        axs[0,2].set_xlabel('R_now');
        axs[1,0].set_xlabel('R_peak/R_now')
        axs[1,1].set_xlabel('R_peak/R_now')
        axs[1,2].set_xlabel('R_peak/R_now')
        
        axs[0,0].hist2d(np.log10(cat['radius']), np.log10(cat['r_peak']), bins=100, cmap='Blues', norm=clr.LogNorm())
        axs[0,1].hist2d(np.log10(cat['radius'][slct_cen]), np.log10(cat['r_peak'][slct_cen]), bins=100, cmap='Blues', norm=clr.LogNorm())
        axs[0,2].hist2d(np.log10(cat['radius'][slct_sat]), np.log10(cat['r_peak'][slct_sat]), bins=100, cmap='Blues', norm=clr.LogNorm())
        axs[1,0].hist(np.log10(cat['r_peak']/cat['radius']), bins=100)
        axs[1,1].hist(np.log10(cat['r_peak'][slct_cen]/cat['radius'][slct_cen]), bins=100)
        axs[1,2].hist(np.log10(cat['r_peak'][slct_sat]/cat['radius'][slct_sat]), bins=100)

        plt.tight_layout()

        plt.show()
        exit()
