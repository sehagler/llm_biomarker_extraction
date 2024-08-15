# -*- coding: utf-8 -*-
"""
Created on Thu Apr 11 09:38:41 2024

@author: haglers
"""

#
import datetime
import itertools
import os
import pickle

#
def get_data(data, key0, key1, biomarker_key, data_key):
    data_list = []
    if data_key in data[key0][key1][biomarker_key].keys():
        data_list.extend(data[key0][key1][biomarker_key][data_key])
    data_list = list(set(data_list))
    if len(data_list) == 0:
        data_list.append('')
    return data_list

#
def generate_main_csv(mode, path, data, filename_base):
    keys_set = { 'percentage', 'score', 'staining', 'strength' }
    data_csv = 'DOCUMENT_ID,DATETIME,Section Title,Specimen Id,PHRASE,BIOMARKER,STATUS,STRENGTH,SCORE,PERCENTAGE,Coords\n'
    keys = data.keys()
    keys = sorted(keys)
    for i in range(len(keys)):
        key0 = keys[i]
        document_id_str = key0[:-4]
        for key1 in data[key0].keys():
            if mode in data[key0][key1].keys():
                if bool(keys_set.intersection(data[key0][key1][mode].keys())):
                    now = datetime.datetime.now()
                    datetime_str = now.strftime("%d-%b-%y %H:%M:%S")
                    section_str = key1
                    specimen_id_str = ''
                    phrase_str = ''
                    biomarker_str = mode
                    percentage_list = get_data(data, key0, key1, mode, 'percentage')
                    score_list = get_data(data, key0, key1, mode, 'score')
                    staining_list = get_data(data, key0, key1, mode, 'staining')
                    strength_list = get_data(data, key0, key1, mode, 'strength')
                    coords_str = '\"[(10, 12)]\"'
                    
                    data_list = [ staining_list, strength_list, score_list, percentage_list ]
                    data_vals = list(itertools.product(*data_list))
                    
                    for data_val in data_vals:
                        csv_tmp = ''
                        csv_tmp += document_id_str + ','
                        csv_tmp += datetime_str + ','
                        csv_tmp += section_str + ','
                        csv_tmp += specimen_id_str + ','
                        csv_tmp += phrase_str + ','
                        csv_tmp += biomarker_str + ','
                        csv_tmp += data_val[0] + ','
                        csv_tmp += data_val[1] + ','
                        csv_tmp += data_val[2] + ','
                        csv_tmp += data_val[3] + ','
                        csv_tmp += coords_str + '\n'
                        data_csv += csv_tmp
            
    with open(os.path.join(path, filename_base + '_' + mode.lower() + '.csv'), 'w') as f:
        f.write(data_csv)

#
def generate_variablity_csv(mode, path, data, filename_base):
    keys_set = { 'variability' }    
    data_csv = 'DOCUMENT_ID,DATETIME,Section Title,Specimen Id,PHRASE,BIOMARKER,VARIABLITY,Coords\n'
    keys = data.keys()
    keys = sorted(keys)
    for i in range(len(keys)):
        key0 = keys[i]
        document_id_str = key0[:-4]
        for key1 in data[key0].keys():
            if mode in data[key0][key1].keys():
                if bool(keys_set.intersection(data[key0][key1][mode].keys())):
                    now = datetime.datetime.now()
                    datetime_str = now.strftime("%d-%b-%y %H:%M:%S")
                    section_str = key1
                    specimen_id_str = ''
                    phrase_str = ''
                    biomarker_str = mode
                    variability_list = get_data(data, key0, key1, mode, 'variability')
                    coords_str = '\"[(10, 12)]\"'
                    
                    for variability_str in variability_list:
                        csv_tmp = ''
                        csv_tmp += document_id_str + ','
                        csv_tmp += datetime_str + ','
                        csv_tmp += section_str + ','
                        csv_tmp += specimen_id_str + ','
                        csv_tmp += phrase_str + ','
                        csv_tmp += biomarker_str + ','
                        csv_tmp += variability_str + ','
                        csv_tmp += coords_str + '\n'
                        data_csv += csv_tmp
            
    with open(os.path.join(path, filename_base + '_variability_' + mode.lower() + '.csv'), 'w') as f:
        f.write(data_csv)

path = '../data_out'
filename_base = 'breast_cancer_biomarkers'

with open(os.path.join(path, filename_base + '_er.pkl'), 'rb') as f:
    data = pickle.load(f)
generate_main_csv('ER', path, data, filename_base)
generate_variablity_csv('ER', path, data, filename_base)

er_data = data

with open(os.path.join(path, filename_base + '_pr.pkl'), 'rb') as f:
    data = pickle.load(f)
generate_main_csv('PR', path, data, filename_base)
generate_variablity_csv('PR', path, data, filename_base)

with open(os.path.join(path, filename_base + '_her2.pkl'), 'rb') as f:
    data = pickle.load(f)
generate_main_csv('HER2', path, data, filename_base)
generate_variablity_csv('HER2', path, data, filename_base)