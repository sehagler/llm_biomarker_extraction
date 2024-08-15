# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 13:15:57 2024

@author: haglers
"""

#
import re

#
class prompts_base_object(object):
    
    #
    def __init__(self, prompt_params):
        self.prompt_params = prompt_params
        self.regex_limit_prefix = '(?<![A-Za-z0-9])'
        self.regex_limit_suffix = '(?![A-Za-z0-9])'
        
    #
    def _clean_result(self, regex, results):
        regex = '(?i)' + regex
        results = list(set(results))
        if 'FALSE_POSITIVE' in results:
            results.remove('FALSE_POSITIVE')
        if len(results) == 0:
            results = None
        if results is not None:
            cleaned_results = []
            for x in results:
                y = re.search(regex, x)
                if y is not None:
                    if len(y.group()) > 0:
                        cleaned_results.append(y.group())
            results = cleaned_results
            if len(results) == 0:
                results = None
        return results
    
    #
    def _clean_results(self, results):
        for key in results.keys():
            results[key] = list(set(results[key]))
        return results

    #
    def _confirm_result(self, text, synonyms_dict, results):
        if results is not None:
            results = list(set(results))
            if len(results) > 1:
                results = list(filter(lambda x: x != "FALSE_POSITIVE", results))
            confirmed_results = []
            for X in results:
                if not bool(synonyms_dict):
                    x_list = [ X ]
                else:
                    if X in synonyms_dict.keys():
                        x_list = synonyms_dict[X]
                    else:
                        x_list = [ X ]
                for x in x_list:
                    regex = self._get_limited_regex(re.escape(x))
                    if re.search(regex, text, re.IGNORECASE):
                        confirmed_results.append(x)
                    else:
                        confirmed_results.append('FALSE_POSITIVE')
            confirmed_results = list(set(confirmed_results))
            if len(confirmed_results) > 1:
                confirmed_results = list(filter(lambda x: x != "FALSE_POSITIVE", confirmed_results))
            if len(confirmed_results) == 1 and confirmed_results[0] == 'FALSE_POSITIVE':
                confirmed_results = None
        else:
            confirmed_results = None
        return confirmed_results
    
    #
    def _expand_result(self, expansion_regex, result_list, text):
        if result_list is not None:
            for i in range(len(result_list)):
                regex = re.escape(result_list[i])
                if expansion_regex['prefix'] is not None:
                    regex = expansion_regex['prefix'] + regex
                if expansion_regex['suffix'] is not None:
                    regex = regex + expansion_regex['suffix']
                regex = '(?i)' + regex
                matches = re.finditer(regex, text)
                match_list = []
                for match in matches:
                    match_list.append(match.group())
                match_list = list(set(match_list))
                match_list = self._get_superstring(match_list)
                if len(match_list) == 1:
                    result_list[i] = match_list[0]
        return result_list
    
    #
    def _extend_results(self, results, result, key):
        if result is not None:
            if key in results.keys():
                results[key].extend(result)
            else:
                results[key] = result
        return results
    
    #
    def _get_limited_regex(self, regex):
        case_0 = '(?<=^)' + regex + '(?=(\s|\n))'
        case_1 = '(?<=(\s|\n))' + regex + '(?=(\s|\n))'
        case_2 = '(?<=(\s|\n))' + regex + '(?=$)'
        limited_regex = '(?i)(' + case_0 + '|' + case_1 + '|' + case_2 + ')'
        return limited_regex
    
    #
    def _get_bounded_neighborhood(self, text, match, regex, radius,
                                  exclusion_dict):
        trim_left_neighborhood_flg = True
        trim_right_neighborhood_flg = True
        length = len(text)
        span = match.span()
        if span[0] <= radius:
            start = 0
        else:
            start = span[0] - radius
        if span[1] + radius < length:
            end = span[1] + radius
        else:
            end = -1
        left_neighborhood = text[start:span[0]]
        if trim_left_neighborhood_flg:
            x = []
            x.append(left_neighborhood.rfind('\n') + 1)
            x.append(left_neighborhood.rfind('.') + 2)
            exclusion_list = exclusion_dict['left_neighborhood']
            if exclusion_list is not None:
                for excluded in exclusion_list:
                    M = re.finditer(self._get_limited_regex(excluded), left_neighborhood)
                    end_list = [m.end(0) + 1 for m in M]
                    if len(end_list) > 0:
                        x.append(max(end_list))
            if len(x) == 0:
                x = -1
            else:
                x = max(x)
            if x != -1:
                left_neighborhood = left_neighborhood[x:]
        left_neighborhood = re.sub(regex, 'MASKED_KEY', left_neighborhood)
        right_neighborhood = text[span[1]:end]
        if trim_right_neighborhood_flg:
            x = []
            #x.append(right_neighborhood.find('\n'))
            exclusion_list = exclusion_dict['right_neighborhood']
            if exclusion_list is not None:
                for excluded in exclusion_list:
                    M = re.finditer(self._get_limited_regex(excluded), right_neighborhood)
                    start_list = [m.start(0) for m in M]
                    if len(start_list) > 0:
                        x.append(min(start_list))
            if len(x) == 0:
                x = -1
            else:
                x = min(x)
            if x != -1:
                right_neighborhood = right_neighborhood[:x]
        right_neighborhood = re.sub(regex, 'MASKED_KEY', right_neighborhood)
        key = text[span[0]:span[1]]
        neighborhood = left_neighborhood + key + right_neighborhood
        neighborhood = re.sub('\n', ' ', neighborhood)
        neighborhood = re.sub(' +', ' ', neighborhood)
        return neighborhood
    
    #
    def _get_full_neighborhood(self, text, match, regex, radius):
        trim_left_neighborhood_flg = True
        trim_right_neighborhood_flg = True
        length = len(text)
        span = match.span()
        if span[0] <= radius:
            start = 0
        else:
            start = span[0] - radius
        if span[1] + radius < length:
            end = span[1] + radius
        else:
            end = -1
        left_neighborhood = text[start:span[0]]
        if trim_left_neighborhood_flg:
            x = []
            x.append(left_neighborhood.rfind('\n') + 1)
            x.append(left_neighborhood.rfind('.') + 2)
            if len(x) == 0:
                x = -1
            else:
                x = max(x)
            if x != -1:
                left_neighborhood = left_neighborhood[x:]
        left_neighborhood = re.sub(regex, 'MASKED_KEY', left_neighborhood)
        right_neighborhood = text[span[1]:end]
        if trim_right_neighborhood_flg:
            x = []
            #x.append(right_neighborhood.find('\n'))
            if len(x) == 0:
                x = -1
            else:
                x = min(x)
            if x != -1:
                right_neighborhood = right_neighborhood[:x]
        right_neighborhood = re.sub(regex, 'MASKED_KEY', right_neighborhood)
        key = text[span[0]:span[1]]
        neighborhood = left_neighborhood + key + right_neighborhood
        neighborhood = re.sub('\n', ' ', neighborhood)
        neighborhood = re.sub(' +', ' ', neighborhood)
        return neighborhood
    
    #
    def _get_superstring(self, result_list):
        input_str_list = result_list
        for i in range(len(input_str_list)):
            input_str_list[i] = input_str_list[i].lower()
        output_str_list = []
        input_str_list = list(set(input_str_list))
        for x in input_str_list:
            not_substring = True
            for y in input_str_list:
                if x != y:
                    if x in y:
                        not_substring = False
            if not_substring:
                output_str_list.append(x)
        result_list = output_str_list
        return result_list
    
    #
    def _get_superstrings(self, results, key):
        if key in results:
            result = self._get_superstring(results[key])
            results[key] = result
        return results