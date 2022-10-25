import matplotlib
import pandas as pd

matplotlib.use('TkAgg')
import numpy as np
from matplotlib import pyplot as plt


base_cleo = '2_test_cleopatra_mongo_'
base_cleo = '3_test_mirador_'
base_mir = '3_test_mirador_'
test_set = [20,40,80,160,320]

base_dir = '/home/salvatore/Documents/ricerca/papers/drafts/2022-cleopatra/ijwgs/experiments/tsung/log2'

parameters = ['tr_change_canvas', 'tr_zoom', 'session', 'page', 'request', 'tr_init_load_page', 'connect', 'tr_change_manually_canvas_2', 'tr_change_manually_canvas']

df = pd.DataFrame( columns=['users', 'time', 'parameter','rate','mean','stddev','max','min','meanfb','countfb'])
df_users = pd.DataFrame( columns=['users', 'time', 'connected'])

for test in test_set:
    start_time = None
    stat_file = open(base_dir+"/"+base_mir+str(test)+"/tsung.log", "r")
    print(base_mir+str(test))
    lines = stat_file.readlines()
    time_stamps = []
    tr_ch_canvas = []
    tr_ch_canvas_bf = []
    tr_ch_canvas_num = []
    connected_users = []
    sessions = []
    for line in lines:
        values = line[line.find(":")+1:].strip()
        values = values.split(" ")
        if "dump" in line:
            if start_time ==  None:
                start_time = float(line.split(" ")[-1])
            elif current_time ==  float(line.split(" ")[-1]) - start_time:
                break
            current_time = float(line.split(" ")[-1]) - start_time
            time_stamps.append(float(line.split(" ")[-1]))
        elif "users " in line:
            row = [test, current_time, float(line.split(" ")[2])]
            df_users = pd.concat([df_users, pd.DataFrame([row],
                                             columns=['users', 'time', 'connected'])])

        elif values[0] in parameters:
            # ($rate,$mean,$stddev,$max,$min,$meanfb,$countfb) = split(/\s+/,$values);
            row = [test, current_time, values[0]]

            float_values = np.array(values[1:]).astype(float)
            row = np.concatenate((row, float_values), axis=None)

            df = pd.concat([df, pd.DataFrame([row],
                                     columns=['users', 'time', 'parameter', 'rate', 'mean', 'stddev', 'max', 'min',
                                              'meanfb', 'countfb'])])

df.to_csv('4_mirador_df_stats.csv')
df_users.to_csv('4_mirador_df_users.csv')





