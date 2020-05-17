#!/usr/bin/env python2.7

from __future__ import print_function, division 

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as  clr
import h5py 
import pandas as pd

import dtk




def load_catalog(fname, step, init_load=False):
    fname = fname.replace("${step}", str(step))
    core_htag = dtk.gio_read(fname, 'fof_halo_tag')
    core_id = dtk.gio_read(fname, 'core_tag')
    core_m_infall = dtk.gio_read(fname, 'infall_tree_node_mass')
    core_radius = dtk.gio_read(fname, "radius")
    core_step   = dtk.gio_read(fname, "infall_step")
    core_x = dtk.gio_read(fname, "x")
    core_y = dtk.gio_read(fname, "y")
    core_z = dtk.gio_read(fname, "z")
    core_htag = dtk.gio_read(fname, 'fof_halo_tag')
    dict_core = {"x" : core_x,
                 "y" : core_y,
                 "z" : core_z,
                 "m_infall" : core_m_infall,
                 "radius" : core_radius,
                 "id" : core_id,
                 "infall_step": core_step,
                 "fof_htag": core_htag,
    }
    if init_load:
        dict_core['m_peak'] = core_m_infall
        dict_core['r_peak'] = core_radius
    print("\tload catalog from",fname," size:",len(core_x))
    return dict_core

def save_catalog(fname, step, dict_core):
    fname = fname.replace("${step}", str(step))
    print("\twriting to",fname)
    hfile = h5py.File(fname, "w")
    for key in dict_core:
        hfile[key] = dict_core[key]
    hfile.close()

def combine_catalogs(current_dict, prev_dict, step, apply_r_peak, apply_m_peak):
    prev_dict_srt = np.argsort(prev_dict['id'])
    index = dtk.search_sorted(prev_dict['id'], current_dict['id'], sorter=prev_dict_srt)
    slct_fnd = index != -1
    m_peak = np.maximum( current_dict['m_infall'][slct_fnd], prev_dict['m_peak'][index[slct_fnd]])
    r_peak = np.maximum( current_dict['radius'][slct_fnd], prev_dict['r_peak'][index[slct_fnd]])
    current_dict["m_peak"] = np.array(current_dict['m_infall'])
    if apply_m_peak:
        current_dict['m_peak'][slct_fnd] = m_peak
    current_dict["r_peak"] = np.array(current_dict['radius'])
    if apply_r_peak:
        current_dict['r_peak'][slct_fnd] = r_peak
    # Central control. R_peak for centrals is r_now
    current_dict['r_peak_raw'] = np.copy(current_dict['r_peak'])
    slct_central = current_dict['infall_step'] == step
    current_dict['r_peak'][slct_central] = current_dict['radius'][slct_central]
    
def preprocess_core_catalog(input_fname, output_fname, steps, apply_r_peak, apply_m_peak):
    prev_dict = load_catalog(input_fname, steps[-1], init_load=True)
    for step in steps[-2::-1]:
        print("working on ", step)
        current_dict = load_catalog(input_fname, step)
        combine_catalogs(current_dict, prev_dict, step, apply_r_peak, apply_m_peak)
        save_catalog(output_fname, step, current_dict)
        prev_dict = current_dict
        # if(step==300):
        #     plt.figure()
        #     plt.hist2d(np.log10(prev_dict['m_infall']), np.log10(prev_dict['m_peak']), bins=100, cmap='Blues', norm=clr.LogNorm())
        #     plt.colorbar()
        #     plt.figure()
        #     plt.hist2d(np.log10(prev_dict['radius']), np.log10(prev_dict['r_peak']), bins=100, cmap='Blues', norm=clr.LogNorm())
        #     plt.colorbar()
        #     plt.show()

if __name__ == "__main__":
    param = dtk.Param(sys.argv[1])
    input_fname = param.get_string("input_fname")
    output_fname = param.get_string("output_fname")
    steps = param.get_int_list("steps")
    apply_r_peak = param.get_bool('r_peak')
    apply_m_peak = param.get_bool('m_peak')
    preprocess_core_catalog(input_fname, output_fname, steps, apply_r_peak, apply_m_peak)
                 

   
