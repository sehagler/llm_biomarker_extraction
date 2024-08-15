# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 12:35:42 2024

@author: haglers
"""

#
import asyncio
import copy
import lmql
import nest_asyncio
import re

#
from lib.prompts_base import prompts_base_object

@lmql.query
async def her2_percentage_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: HER2 Equivocal ( 2+ ) see results of BDISH below > 10%\n"
    "ANSWER: HER2 value is 10%\n"
    "EXAMPLE: HER2 Positive ( 3+ ) ( > 95%\n"
    "ANSWER: HER2 value is 95%\n"
    "EXAMPLE: HER2 negative ( 1+ ) < 1%\n"
    "ANSWER: HER2 value is 1%\n"
    "EXAMPLE: HER2 Negative ( 0 , < 10%\n"
    "ANSWER: HER2 value is 10%\n"
    "EXAMPLE: HER2 membrane staining : 40%\n"
    "ANSWER: HER2 value is 40%\n"
    "EXAMPLE: HER2 Negative 0%\n"
    "ANSWER: HER2 value is 0%\n"
    "EXAMPLE: HER2 0%\n"
    "ANSWER: HER2 value is 0%\n"
    "EXAMPLE: HER2 50%\n"
    "ANSWER: HER2 value is 50%\n"
    "EXAMPLE: HER2 100%\n"
    "ANSWER: HER2 value is 100%\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: HER2 value is [CLS]\n" where STOPS_AT(CLS, '.') and REGEX(CLS, r"(?i)([0-9]{1,2}%|100%)")
    from prompt_params['lmql_model']
    '''

@lmql.query
async def her2_score_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: HER2 Equivocal ( weak 2+\n"
    "ANSWER: HER2 value is 2+\n"
    "EXAMPLE: HER2 Positive ( 3+\n"
    "ANSWER: HER2 value is 3+\n"
    "EXAMPLE: HER2 Negative ( 1+\n"
    "ANSWER: HER2 value is 1+\n"
    "EXAMPLE: HER2 negative ( 0\n"
    "ANSWER: HER2 value is 0\n"
    "EXAMPLE: HER2 Equivocal ( 2\n"
    "ANSWER: HER2 value is 2\n"
    "EXAMPLE: HER2 4B5 Negative 1+\n"
    "ANSWER: HER2 value is 1+\n"
    "EXAMPLE: HER2 4B5 Equivocal 2+\n"
    "ANSWER: HER2 value is 2+\n"
    "EXAMPLE: HER2 Equivocal ( 2\n"
    "ANSWER: HER2 value is 2\n"
    "EXAMPLE: HER2 4B5 1+\n"
    "ANSWER: HER2 value is 1+\n"
    "EXAMPLE: HER2 ( 0\n"
    "ANSWER: HER2 value is 0\n"
    "EXAMPLE: HER2 1\n"
    "ANSWER: HER2 value is 1\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: HER2 value is [CLS]\n" where STOPS_AT(CLS, '.') and REGEX(CLS, r"(?i)[0-4](\+)?")
    from prompt_params['lmql_model']
    '''

@lmql.query
async def her2_staining_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: HER2 overexpression : Absent\n"
    "ANSWER: HER2 value is absent\n"
    "EXAMPLE: HER2 4B5 Negative\n"
    "ANSWER: HER2 value is negative\n"
    "EXAMPLE: negative for HER2\n"
    "ANSWER: HER2 value is negative\n"
    "EXAMPLE: negative for HER2\n"
    "ANSWER: HER2 value is negative\n"
    "EXAMPLE: negativity for HER2\n"
    "ANSWER: HER2 value is negativity\n"
    "EXAMPLE: positive for HER2\n"
    "ANSWER: HER2 value is positive\n"
    "EXAMPLE: positivity for HER2\n"
    "ANSWER: HER2 value is positivity\n"
    "EXAMPLE: HER2 Negative\n"
    "ANSWER: HER2 value is negative\n"
    "EXAMPLE: HER2 Positive\n"
    "ANSWER: HER2 value is positive\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.')
    "ANSWER: HER2 value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["absent", "negative", "negativity", "positive", "positivity"])
    from prompt_params['lmql_model']
    '''

@lmql.query
async def her2_staining_amplified_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: non - amplified for HER2\n"
    "ANSWER: HER2 value is amplified\n"
    "EXAMPLE: amplified for HER2\n"
    "ANSWER: HER2 value is amplified\n"
    "EXAMPLE: HER2 amplified\n"
    "ANSWER: HER2 value is amplified\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.')
    "ANSWER: HER2 value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["amplified"])
    from prompt_params['lmql_model']
    '''

@lmql.query
async def her2_staining_equivocal_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: HER2 Equivocal\n"
    "ANSWER: HER2 value is equivocal\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.')
    "ANSWER: HER2 value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["equivocal"])
    from prompt_params['lmql_model']
    '''

@lmql.query
async def her2_variability_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: HER2 variable\n"
    "ANSWER: HER2 value is variable\n"
    "EXAMPLE: variable HER2\n"
    "ANSWER: HER2 value is variable\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: HER2 value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["variable"])
    from prompt_params['lmql_model']
    '''
    
#
class Her2_prompts_object(prompts_base_object):
    
    #
    async def _her2_percentage_prompt(self, prompt_params):
        result = await her2_percentage_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _her2_score_prompt(self, prompt_params):
        result = await her2_score_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _her2_staining_prompt(self, prompt_params):
        result = await her2_staining_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _her2_staining_amplified_prompt(self, prompt_params):
        result = await her2_staining_amplified_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _her2_staining_equivocal_prompt(self, prompt_params):
        result = await her2_staining_equivocal_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _her2_variability_prompt(self, prompt_params):
        result = await her2_variability_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    def _prompt_her2_percentage(self, prompt_params, neighborhood):
        regex = '([0-9]{1,2}|100)%'
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = {}
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'], prompt_params['neighborhood']):
            prompt_params_trimmed = copy.deepcopy(prompt_params)
            trimmed_neighborhood = re.sub(' \- ([0-9]{1,2}|100)%', '', neighborhood)
            prompt_params_trimmed['neighborhood'] = trimmed_neighborhood
            prompt_result = \
                asyncio.run(self._her2_percentage_prompt(prompt_params_trimmed))
            result = [ prompt_result.variables['CLS'] ]
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
            expansion_regex = {}
            expansion_regex['prefix'] = '((~|>|<) )?'
            expansion_regex['suffix'] = '( \- ([0-9]{1,2}|100)%)?( HER2)?'
            result = \
                self._expand_result(expansion_regex, result, neighborhood)
            if result is not None:
                trimmed_result = []
                for i in range(len(result)):
                    if 'her2' not in result[i].lower():
                        trimmed_result.append(result[i])
                result = trimmed_result
                if len(result) == 0:
                    result = None
            if result is not None:
                for i in range(len(result)):
                    result[i] = re.sub(' \- ', '-', result[i])
        else:
            result = None
        return result
    
    #
    def _prompt_her2_score(self, prompt_params, neighborhood):
        regex = '[0-4](\+)?'
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = {}
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'], prompt_params['neighborhood']):
            prompt_params_trimmed = copy.deepcopy(prompt_params)
            trimmed_neighborhood = re.sub(' \- [0-4](\+)?', '', neighborhood)
            prompt_params_trimmed['neighborhood'] = trimmed_neighborhood
            prompt_result = \
                asyncio.run(self._her2_score_prompt(prompt_params_trimmed))
            result = [ prompt_result.variables['CLS'] ]
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
            expansion_regex = {}
            expansion_regex['prefix'] = '(grade )?((~|>|<) )?'
            expansion_regex['suffix'] = '( \- [0-4](\+)?)?'
            result = \
                self._expand_result(expansion_regex, result, neighborhood)
            if result is not None:
                trimmed_result = []
                for i in range(len(result)):
                    if 'grade' not in result[i].lower():
                        trimmed_result.append(result[i])
                result = trimmed_result
                if len(result) == 0:
                    result = None
            if result is not None:
                for i in range(len(result)):
                    result[i] = re.sub(' \- ', '-', result[i])
        else:
            result = None
        return result
    
    #
    def _prompt_her2_staining(self, prompt_params, neighborhood):
        regex = '(?i)(absent|amplified|equivocal|negative|negativity|positive|positivity)'
        synonyms_dict = {}
        synonyms_dict['negative'] = [ 'negative', 'negativity' ]
        synonyms_dict['positive'] = [ 'positive', 'positivity' ]
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = synonyms_dict
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'], prompt_params['neighborhood']):
            result = []
            if re.search('(?i)(absent|negative|negativity|positive|positivity)', prompt_params['neighborhood']):
                prompt_result = \
                    asyncio.run(self._her2_staining_prompt(prompt_params))
                result.append(prompt_result.variables['CLS'])
            if re.search('(?i)amplified', prompt_params['neighborhood']):
                prompt_result = \
                    asyncio.run(self._her2_staining_amplified_prompt(prompt_params))
                result.append(prompt_result.variables['CLS'])
            if re.search('(?i)equivocal', prompt_params['neighborhood']):
                prompt_result = \
                    asyncio.run(self._her2_staining_equivocal_prompt(prompt_params))
                result.append(prompt_result.variables['CLS'])
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
            expansion_regex = {}
            expansion_regex['prefix'] = '((diffusely|focal(ly)?|low|minimally|present and) )?((non \-|not) )?'
            expansion_regex['suffix'] = '( for malignancy)?'
            result = \
                self._expand_result(expansion_regex, result, neighborhood)
            if result is not None:
                trimmed_result = []
                for i in range(len(result)):
                    if 'present and' not in result[i].lower() and \
                       'for malignancy' not in result[i].lower():
                        trimmed_result.append(result[i])
                result = trimmed_result
                if len(result) == 0:
                    result = None
            if result is not None:
                for i in range(len(result)):
                    result[i] = re.sub(' \- ', '-', result[i])
                    result[i] = re.sub('(?i)absent', 'negative', result[i])
                    result[i] = re.sub('(?i)not amplified', 'non-amplified', result[i])
                    result[i] = re.sub('(?i)focal ', 'focally ', result[i])
        else:
            result = None
        return result
    
    #
    def _prompt_her2_variability(self, prompt_params, neighborhood):
        regex = '(?i)variable'
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = {}
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'], prompt_params['neighborhood']):
            prompt_result = \
                asyncio.run(self._her2_variability_prompt(prompt_params))
            result = [ prompt_result.variables['CLS'] ]
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
        else:
            result = None
        return result
    
    #
    def run_prompts(self, text, exclusion_dict):
        nest_asyncio.apply()
        results = {}
        regex = self._get_limited_regex('HER2')
        M = re.finditer(regex, text)
        if M:
            for m in M:
                neighborhood = \
                    self._get_bounded_neighborhood(text, m, regex,
                                                   self.prompt_params['radius'],
                                                   exclusion_dict)
                excluded_regex = '(if|interpret(ed)?|ventana\'?s?)'
                excluded_regex = self._get_limited_regex(excluded_regex)
                if not re.search(excluded_regex, neighborhood):
                    neighborhood = \
                        re.sub('(?i)(negative|positive)( ,)? HER2', 'HER2', neighborhood)
                    result = self._prompt_her2_percentage(self.prompt_params, neighborhood)
                    results = self._extend_results(results, result, 'percentage')
                    result = self._prompt_her2_score(self.prompt_params, neighborhood)
                    results = self._extend_results(results, result, 'score')
                    result = self._prompt_her2_staining(self.prompt_params, neighborhood)
                    results = self._extend_results(results, result, 'staining')
                    result = self._prompt_her2_variability(self.prompt_params, neighborhood)
                    results = self._extend_results(results, result, 'variability')
            results = self._clean_results(results)
            if 'staining' in results.keys():
                if 'amplified' in results['staining'] and \
                   'non-amplified' in results['staining']:
                    results['staining'].remove('amplified')
            results = self._get_superstrings(results, 'staining')
        if not bool(results):
            results = None
        return results