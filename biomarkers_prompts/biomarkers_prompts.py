# -*- coding: utf-8 -*-
"""
Created on Mon Jan  8 15:01:22 2024

@author: haglers
"""

import argparse
import html
import lmql
import os
import pickle
import re
import xml.etree.ElementTree as ET

from lib.er_prompts import Er_prompts_object
from lib.pr_prompts import Pr_prompts_object
from lib.her2_prompts import Her2_prompts_object

#
def section_text(sections_regex, text):
    sectioned_text = {}
    text_list = text.split('\n\n')
    header = None
    text = None
    for j in range(len(text_list)):
        test_text = text_list[j]
        if re.match(sections_regex, test_text):
            if text is not None:
                sectioned_text[header] = text[1:]
            header = test_text
            text = ''
        else:
            text += '\n'
            text += test_text
        sectioned_text[header] = text[1:]
    return sectioned_text

#
def run_prompts(prompt_params):
    er_prompts_object = Er_prompts_object(prompt_params)
    pr_prompts_object = Pr_prompts_object(prompt_params)
    her2_prompts_object = Her2_prompts_object(prompt_params)
    filenames = os.listdir(prompt_params['data'])
    filenames = sorted(filenames)
    with open(prompt_params['keywords'])as f:
        sections = f.read()
    section_list = sections.split('\n')
    del section_list[-1]
    sections_regex = "(" + "|".join(section_list) + ")"
    print(len(filenames), flush=prompt_params['debug'])
    results = {}
    for i in range(len(filenames)):
        filename = filenames[i]
        results[filename] = {}
        rpt_str = 'num: ' + str(i) +' file: ' + filename
        print(rpt_str, flush=prompt_params['debug'])
        parser = ET.iterparse(os.path.join(prompt_params['data'], filename))
        for event, elem in parser:
            if elem.tag == 'rpt_text':
                text = elem.text
        sectioned_text = section_text(sections_regex, text)
        keys = list(sectioned_text.keys())
        for j in range(len(keys)):
            header = keys[j]
            text = html.unescape(sectioned_text[header])
            text = re.sub('&gt;', '>', text)
            text = re.sub('&lt;', '<', text)
            text = re.sub('\(', ' ( ', text)
            text = re.sub('\)', ' ) ', text)
            text = re.sub('\-', ' - ', text)
            text = re.sub(' +', ' ', text)
            text = re.sub('(?<=[0-4]) \+', '+', text)
            text = re.sub('WT \- 1', 'WT-1', text)
            if prompt_params['mode'] == 'ER':
                exclusion_dict = {}
                exclusion_dict['left_neighborhood'] = [ '\)', 'ER', 'HER2', 'KI67', 'PR' ]
                exclusion_dict['right_neighborhood'] = [ 'ER', 'HER2', 'KI67', 'PR', 'present and positive' ]
                result = er_prompts_object.run_prompts(text, exclusion_dict)
            elif prompt_params['mode'] == 'PR':
                exclusion_dict = {}
                exclusion_dict['left_neighborhood'] = [ '\)', 'ER', 'HER2', 'KI67', 'PR' ]
                exclusion_dict['right_neighborhood'] = [ 'ER', 'HER2', 'KI67', 'PR', 'present and positive' ]
                result = pr_prompts_object.run_prompts(text, exclusion_dict)
            elif prompt_params['mode'] == 'HER2':
                exclusion_dict = {}
                exclusion_dict['left_neighborhood'] = [ '\)', 'ER', 'HER2', 'KI67', 'PR' ]
                exclusion_dict['right_neighborhood'] = [ 'comment', 'ER', 'HER2', 'KI67', 'PR' ]
                result = her2_prompts_object.run_prompts(text, exclusion_dict)
            else:
                result = None
            if result is not None:
                if header not in list(results[filename].keys()):
                    results[filename][header] = {}
                results[filename][header][prompt_params['mode']] = \
                    result
        if i % 10 == 9:
            pickle.dump(results, open(prompt_params['pickle'], "wb"))
    pickle.dump(results, open(prompt_params['pickle'], "wb"))

#
def main():
    parser = \
        argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--cuda', action='store_true',
                        help='Set to use GPUs')
    parser.add_argument('--data', type=str, nargs=1,
                        help='Data directory')
    parser.add_argument('--keywords', type=str, nargs=1,
                        help='Keywords file')
    parser.add_argument('--layout', type=str, nargs=1,
                        help='The gpu layout being used')
    parser.add_argument('--mode', type=str, nargs=1,
                        help='The mode being used')
    parser.add_argument('--model', type=str, nargs=1,
                        help='The model being used')
    parser.add_argument('--pickle', type=str, nargs=1,
                        help='The pickle file name')
    parser.add_argument('--port', type=str, nargs=1,
                        help='The port being used')
    parser.add_argument('--tokenizer', type=str, nargs=1,
                        help='The tokenizer being used')
    args = parser.parse_args()
    prompt_params = {}
    prompt_params['data'] = args.data[0]
    prompt_params['debug'] = False
    prompt_params['keywords'] = args.keywords[0]
    prompt_params['max_len'] = 32768
    prompt_params['mode'] = args.mode[0]
    prompt_params['model'] = 'local:llama.cpp:' + args.model[0]
    prompt_params['n_ctx'] = 32768
    prompt_params['pickle'] = args.pickle[0]
    prompt_params['port'] = 'localhost:' + args.port[0]
    prompt_params['radius'] = 150
    prompt_params['tokenizer'] = args.tokenizer[0]
    if args.cuda:
        prompt_params['cuda'] = args.cuda
        prompt_params['layout'] = args.layout[0]
        prompt_params['lmql_model'] = \
            lmql.model(model_identifier=prompt_params['model'],
                       tokenizer=prompt_params['tokenizer'],
                       cuda=prompt_params['cuda'],
                       layout=prompt_params['layout'],
                       n_ctx=prompt_params['n_ctx'])
    else:
        prompt_params['lmql_model'] = \
            lmql.model(model_identifier=prompt_params['model'],
                       tokenizer=prompt_params['tokenizer'],
                       n_ctx=prompt_params['n_ctx'])
    run_prompts(prompt_params)

#
if __name__ == "__main__":
    main()