import os
import json
import pandas as pd
import numpy as np
from pygama import __version__ as pygama_version
import pygama
import pygama.lgdo as lgdo
import pygama.lgdo.lh5_store as lh5
from os.path import expanduser
import copy




def get_t2_data(run, tab=None):
    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    t2_dir = data['tier2_dir']
    f_raw = t2_dir + "/Run" + str(run)+ '.lh5'
    raw_store = lh5.LH5Store()
    lh5_file = raw_store.gimme_file(f_raw, 'r')

    lh5_tables = []
    lh5_keys = lh5.ls(f_raw)

    if tab == None:
        for tb in lh5_keys:
            if "dsp" not in tb:
                tbname = raw_store.ls(lh5_file[tb])[0]
            if "dsp" in tbname:
                tb = tb + '/' + tbname  # g024 + /dsp
            lh5_tables.append(tb)

        lh5_tables.pop(-1)
    elif type(tab) != list:
        if tab in lh5_keys:
            lh5_tables.append(tab)
        else:
            print(tab, "table not in list")
            exit()
    elif type(tab) == list:
        for tb in tab:
            if tb in list:
                if "dsp" not in tb:
                    tbname = raw_store.ls(lh5_file[tb])[0]
                if "dsp" in tbname:
                    tb = tb + '/' + tbname  # g024 + /dsp
                lh5_tables.append(tb)
            else:
                print(tab, "table not in list")
                exit()

    buffer_len = 10000000000000000
    t2_data = []
    for tb in lh5_tables:
        # load primary table and build processing chain and output table
        tot_n_rows = raw_store.read_n_rows(tb, f_raw)

        chan_name = tb.split('/')[0]
        t2_noise, n_rows_read = raw_store.read_object(tb, f_raw, start_row=0, n_rows=buffer_len)
        t2_data.append(t2_noise)

        return t2_data


def get_t1_data(run, tab=None):
    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    t1_dir = data['tier1_dir']


    f_raw = t1_dir + '/Run' + str(run) + '.lh5'
    raw_store = lh5.LH5Store()
    lh5_file = raw_store.gimme_file(f_raw, 'r')

    lh5_tables = []
    lh5_keys = lh5.ls(f_raw)


    if tab == None:
        lh5_tables = lh5.ls(f_raw)
    elif type(tab) != list:
        if tab in lh5_keys:
            lh5_tables.append(tab)
        else:
            print(tab, "table not in list")
            exit()
    elif type(tab) == list:
        for tb in tab:
            if tb in lh5_keys:
                lh5_tables.append(tb)
            else:
                print(tab, "table not in list")
                exit()

    buffer_len = 10000000000000000
    t1_data = []
    for tb in lh5_tables:
        # load primary table and build processing chain and output table
        tot_n_rows = raw_store.read_n_rows(tb, f_raw)

        chan_name = tb.split('/')[0]
        t1_noise, n_rows_read = raw_store.read_object(tb, f_raw, start_row=0, n_rows=buffer_len)
        t1_data.append(t1_noise)


    return t1_data


def get_t2_data_multiple(runs):
    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    t2_dir = data['tier2_dir']
    f_raw = t2_dir + '/Run' + str(runs[0])
    raw_store = lh5.Store()
    lh5_file = raw_store.gimme_file(f_raw, 'r')

    lh5_tables = []
    lh5_keys = raw_store.ls(f_raw)

    for tb in lh5_keys:
        if "dsp" not in tb:
            tbname = raw_store.ls(lh5_file[tb])[0]
        if "dsp" in tbname:
            tb = tb + '/' + tbname  # g024 + /dsp
        lh5_tables.append(tb)

    lh5_tables.pop(-1)

    buffer_len = 10000000000000000
    for tb in lh5_tables:
        # load primary table and build processing chain and output table
        tot_n_rows = raw_store.read_n_rows(tb, f_raw)

        chan_name = tb.split('/')[0]
        t2_noise, n_rows_read = raw_store.read_object(
            tb, f_raw, start_row=0, n_rows=buffer_len)

    for run in runs:
        f_raw = t2_dir + '/Run' + str(run)
        raw_store = lh5.Store()
        lh5_file = raw_store.gimme_file(f_raw, 'r')

        lh5_tables = []
        lh5_keys = raw_store.ls(f_raw)

        for tb in lh5_keys:
            if "dsp" not in tb:
                tbname = raw_store.ls(lh5_file[tb])[0]
            if "dsp" in tbname:
                tb = tb + '/' + tbname  # g024 + /dsp
            lh5_tables.append(tb)

        lh5_tables.pop(-1)

        buffer_len = 10000000000000000
        for tb in lh5_tables:
            # load primary table and build processing chain and output table
            tot_n_rows = raw_store.read_n_rows(tb, f_raw)

            chan_name = tb.split('/')[0]
            t2_noise[run], n_rows_read = raw_store.read_object(
                tb, f_raw, start_row=0, n_rows=buffer_len)

    return t2_noise


def get_t1_data_multiple(runs):
    cwd = os.getcwd()
    file = cwd + '/address.json'
    with open(file, 'r') as read_file:
        data = json.load(read_file)

    t1_dir = data['tier1_dir']

    f_raw = t1_dir + '/Run' + str(runs[0])
    raw_store = lh5.Store()
    lh5_file = raw_store.gimme_file(f_raw, 'r')

    lh5_tables = []
    lh5_keys = raw_store.ls(f_raw)

    for tb in lh5_keys:
        if "raw" not in tb:
            tbname = raw_store.ls(lh5_file[tb])[0]
        if "raw" in tbname:
            tb = tb + '/' + tbname  # g024 + /dsp
        lh5_tables.append(tb)


    buffer_len = 10000000000000000
    for tb in lh5_tables:
        # load primary table and build processing chain and output table
        tot_n_rows = raw_store.read_n_rows(tb, f_raw)

        chan_name = tb.split('/')[0]
        t2_noise, n_rows_read = raw_store.read_object(
            tb, f_raw, start_row=0, n_rows=buffer_len)

    for run in runs:
        f_raw = t1_dir + '/Run' + str(run)
        raw_store = lh5.Store()
        lh5_file = raw_store.gimme_file(f_raw, 'r')

        lh5_tables = []
        lh5_keys = raw_store.ls(f_raw)

        for tb in lh5_keys:
            if "raw" not in tb:
                tbname = raw_store.ls(lh5_file[tb])[0]
            if "raw" in tbname:
                tb = tb + '/' + tbname  # g024 + /dsp
            lh5_tables.append(tb)


        buffer_len = 10000000000000000
        for tb in lh5_tables:
            # load primary table and build processing chain and output table
            tot_n_rows = raw_store.read_n_rows(tb, f_raw)

            chan_name = tb.split('/')[0]
            # db_dict = database.get(chan_name) if database else None
            t1_noise[run], n_rows_read = raw_store.read_object(
                tb, f_raw, start_row=0, n_rows=buffer_len)

    return t1_noise


def get_df(run, tab=None):
    data = get_t2_data(run, tab)
    dictionary = dict()
    for col in data[0]:
        dictionary[col] = data[0][col].nda

    df = pd.DataFrame(data=dictionary)
    return df

def get_df_multiple(runs, tb=None):
    lis = []
    for run in runs:
        df = get_df(run, tb)
        lis.append(df)

    dictionary = pd.concat(lis)
    dictionary = dictionary.reset_index(drop=True)
    return dictionary
