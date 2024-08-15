# -*- coding: utf-8 -*-
"""
Created on Tue May 14 17:58:30 2024

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
async def pr_percentage_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: PR ( 16 ) positive ( 2+ , > 80%\n"
    "ANSWER: PR value is 80%\n"
    "EXAMPLE: PR strongly positive ( strong immunoreactivity in > 75%\n"
    "ANSWER: PR value is 75%\n"
    "EXAMPLE: PR % invasive tumor cells staining : > 95%\n"
    "ANSWER: PR value is 95%\n"
    "EXAMPLE: PR ( 1E2 ) Negative ( < 1%\n"
    "ANSWER: PR value is 1%\n"
    "EXAMPLE: PR ( 1E2 ) Positive ( > 95%\n"
    "ANSWER: PR value is 95%\n"
    "EXAMPLE: PR ( 1E2 ) positive , 90%\n"
    "ANSWER: PR value is 90%\n"
    "EXAMPLE: PR ( 1E2 ) Positive ( 50%\n"
    "ANSWER: PR value is 50%\n"
    "EXAMPLE: 80% positivity for ER and PR\n"
    "ANSWER: PR value is 80%\n"
    "EXAMPLE: PR 1E2 Negative < 2%"
    "ANSWER: PR value is 2%"
    "EXAMPLE: PR 1E2 Positive > 95%\n"
    "ANSWER: PR value is 95%\n"
    "EXAMPLE: PR 1E2 positive ( 100%\n"
    "ANSWER: PR value is 100%\n"
    "EXAMPLE: PR 1E2 Positive 10%\n"
    "ANSWER: PR value is 10%\n"
    "EXAMPLE: PR 0%\n"
    "ANSWER: PR value is 0%\n"
    "EXAMPLE: PR 50%\n"
    "ANSWER: PR value is 50%\n"
    "EXAMPLE: PR 100%\n"
    "ANSWER: PR value is 100%\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and REGEX(CLS, r"(?i)([0-9]{1,2}%|100%)")
    from prompt_params['lmql_model']
    '''
    
@lmql.query
async def pr_percentage_er_and_pr_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: 80% positivity for ER and PR\n"
    "ANSWER: PR value is 80%\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and REGEX(CLS, r"(?i)([0-9]{1,2}%|100%)")
    from prompt_params['lmql_model']
    '''

@lmql.query
async def pr_score_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: PR ( 16 ) Positive 10% - 20% of DCIS , 2\n"
    "ANSWER: PR value is 2\n"
    "EXAMPLE: PR 1E2 Positive 10% - 20% of DCIS , 2+\n"
    "ANSWER: PR value is 2+\n"
    "EXAMPLE: PR 1E2 Positive > 80% of tumor cells , 2\n"
    "ANSWER: PR value is 2\n"
    "EXAMPLE: PR ( 1E2 ) positive ( 95% , 3+\n"
    "ANSWER: PR value is 3+\n"
    "EXAMPLE: PR 1E2 Positive > 95% of cells , 3+\n"
    "ANSWER: PR value is 3+\n"
    "EXAMPLE: PR 1E2 Positive > 95% of tumor , 3+\n"
    "ANSWER: PR value is 3+\n"
    "EXAMPLE: PR 1E2 Negative <; 2% variable , 3+\n"
    "ANSWER: PR value is 3+\n"
    "EXAMPLE: PR 1E2 Positive variable , ~ 10% 3+\n"
    "ANSWER: PR value is 3+\n"
    "EXAMPLE: PR 1E2 Negative variable , 1% , 3+\n"
    "ANSWER: PR value is 3+\n"
    "EXAMPLE: PR 1E2 Negative < 2% , 1\n"
    "ANSWER: PR value is 1\n"
    "EXAMPLE: PR ( 16 ) positive ( 2+\n"
    "ANSWER: PR value is 2+\n"
    "EXAMPLE: PR ( 16 ) negative , 0+\n"
    "ANSWER: PR value is 0+\n"
    "EXAMPLE: 3 for PR\n"
    "ANSWER: PR value is 3\n"
    "EXAMPLE: PR ( 0\n"
    "ANSWER: PR value is 0\n"
    "EXAMPLE: PR 1E2 1+\n"
    "ANSWER: PR value is 1+\n"
    "EXAMPLE: PR 1\n"
    "ANSWER: PR value is 1\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and REGEX(CLS, r"(?i)[0-4](\+)?")
    from prompt_params['lmql_model']
    '''
    
@lmql.query
async def pr_score_er_and_pr_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: 3+ , 80% positivity for ER and PR\n"
    "ANSWER: PR value is 3+\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and REGEX(CLS, r"(?i)[0-4](\+)?")
    from prompt_params['lmql_model']
    '''

@lmql.query
async def pr_staining_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: PR 1E6 Carcinoma In Situ : Negative\n"
    "ANSWER: PR value is negative\n"
    "EXAMPLE: PR SP1 Invasive Carcinoma : Positive\n"
    "ANSWER: PR value is positive\n"
    "EXAMPLE: PR ( SP1 ) Weakly positive\n"
    "ANSWER: PR value is positive\n"
    "EXAMPLE: PR ( 6F11 ) 2+ Positive\n"
    "ANSWER: PR value is positive\n"
    "EXAMPLE: PR ( 1E2 ) positive\n"
    "ANSWER: PR value is positive\n"
    "EXAMPLE: negative for ER and PR\n"
    "ANSWER: PR value is negative\n"
    "EXAMPLE: positivity for ER and PR\n"
    "ANSWER: PR value is positivity\n"
    "EXAMPLE: PR SP1 2+ Negative\n"
    "ANSWER: PR value is negative\n"
    "EXAMPLE: negativity for PR\n"
    "ANSWER: PR value is negativity\n"
    "EXAMPLE: positivity for PR\n"
    "ANSWER: PR value is positivity\n"
    "EXAMPLE: positive for PR\n"
    "ANSWER: PR value is positive\n"
    "EXAMPLE: PR strongly positive\n"
    "ANSWER: PR value is positive\n"
    "EXAMPLE: PR 1E2 Negative\n"
    "ANSWER: PR value is negative\n"
    "EXAMPLE: PR 98% Favorable\n"
    "ANSWER: PR value is favorable\n"
    "EXAMPLE: PR favorable\n"
    "ANSWER: PR value is favorable\n"
    "EXAMPLE: PR negative\n"
    "ANSWER: PR value is negative\n"
    "EXAMPLE: PR positive\n"
    "ANSWER: PR value is positive\n"
    "EXAMPLE: PR unfavorable\n"
    "ANSWER: PR value is unfavorable\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["favorable", "negative", "negativity", "positive", "positivity", "unfavorable"])
    from prompt_params['lmql_model']
    '''
    
@lmql.query
async def pr_staining_er_and_pr_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: negative for ER and PR\n"
    "ANSWER: PR value is negative\n"
    "EXAMPLE: positive for ER and PR\n"
    "ANSWER: PR value is positive\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["favorable", "negative", "negativity", "positive", "positivity", "unfavorable"])
    from prompt_params['lmql_model']
    '''

@lmql.query
async def pr_strength_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: PR ( 1E2 ) Very focally positive ( ~ 1% moderate\n"
    "ANSWER: PR value is moderate\n"
    "EXAMPLE: PR ( 1E2 ) Positive ( 1% - 5% , strong\n"
    "ANSWER: PR value is strong\n"
    "EXAMPLE: PR ( 1E2 ) Positive ( ~ 10% , weak\n"
    "ANSWER: PR value is weak\n"
    "EXAMPLE: PR ( 16 ) Positive ( > 90% , moderate\n"
    "ANSWER: PR value is moderate\n"
    "EXAMPLE: PR ( 1E2 ) Negative ( < 1% , strong\n"
    "ANSWER: PR value is strong\n"
    "EXAMPLE: PR ( 16 ) positive , 90% , strong\n"
    "ANSWER: PR value is strong\n"
    "EXAMPLE: PR ( 1E2 ) positive ( variable strong\n"
    "ANSWER: PR value is strong\n"
    "EXAMPLE: strongly diffusely positive for ER and PR\n"
    "ANSWER: PR value is strongly\n"
    "EXAMPLE: PR ( 16 ) Weakly\n"
    "ANSWER: PR value is weakly\n"
    "EXAMPLE: PR ( 1E2 ) moderate\n"
    "ANSWER: PR value is moderate\n"
    "EXAMPLE: PR ( 1E2 ) strong\n"
    "ANSWER: PR value is strong\n"
    "EXAMPLE: strong diffusely positive PR\n"
    "ANSWER: PR value is strong\n"
    "EXAMPLE: strongly positive for PR\n"
    "ANSWER: PR value is strongly\n"
    "EXAMPLE: PR 1E2 weak\n"
    "ANSWER: PR value is weak\n"
    "EXAMPLE: PR moderate\n"
    "ANSWER: PR value is moderate\n"
    "EXAMPLE: PR strong\n"
    "ANSWER: PR value is strong\n"
    "EXAMPLE: PR strongly\n"
    "ANSWER: PR value is strongly\n"
    "EXAMPLE: PR weak\n"
    "ANSWER: PR value is weak\n"
    "EXAMPLE: PR weakly\n"
    "ANSWER: PR value is weakly\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.')
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["moderate", "strong", "strongly", "weak", "weakly"])
    from prompt_params['lmql_model']
    '''
    
@lmql.query
async def pr_strength_er_and_pr_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: strongly diffusely positive for ER and PR\n"
    "ANSWER: PR value is strongly\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.')
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["moderate", "strong", "strongly", "weak", "weakly"])
    from prompt_params['lmql_model']
    '''

@lmql.query
async def pr_strength_zero_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE:PR ( 1E2 ) Negative ( No staining\n"
    "ANSWER: PR value is no"
    "EXAMPLE: PR 1E2 Negative zero staining\n"
    "ANSWER: PR value is zero\n"
    "EXAMPLE: PR 16 Negative zero staining\n"
    "ANSWER: PR value is zero\n"
    "EXAMPLE: PR zero staining\n"
    "ANSWER: PR value is zero\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.')
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["no", "zero"])
    from prompt_params['lmql_model']
    '''

@lmql.query
async def pr_variability_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: PR ( 1E2 ) Focally positive ( variable\n"
    "ANSWER: PR value is variable\n"
    "EXAMPLE: PR ( 16 ) positive ( variable\n"
    "ANSWER: PR value is variable\n"
    "EXAMPLE: PR ( 1E2 ) positive ( variable\n"
    "ANSWER: PR value is variable\n"
    "EXAMPLE: PR ( 1E2 ) variable\n"
    "ANSWER: PR value is variable\n"
    "EXAMPLE: PR variable\n"
    "ANSWER: PR value is variable\n"
    "EXAMPLE: variable PR\n"
    "ANSWER: PR value is variable\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: PR value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["variable"])
    from prompt_params['lmql_model']
    '''

#
class Pr_prompts_object(prompts_base_object):

    #
    async def _pr_percentage_prompt(self, prompt_params):
        result = await pr_percentage_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _pr_percentage_er_and_pr_prompt(self, prompt_params):
        result = await pr_percentage_er_and_pr_prompt(prompt_params, prompt_params['neighborhood'])
        return result

    #
    async def _pr_score_prompt(self, prompt_params):
        result = await pr_score_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _pr_score_er_and_pr_prompt(self, prompt_params):
        result = await pr_score_er_and_pr_prompt(prompt_params, prompt_params['neighborhood'])
        return result

    #
    async def _pr_staining_prompt(self, prompt_params):
        result = await pr_staining_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _pr_staining_er_and_pr_prompt(self, prompt_params):
        result = await pr_staining_er_and_pr_prompt(prompt_params, prompt_params['neighborhood'])
        return result

    #
    async def _pr_strength_prompt(self, prompt_params):
        result = await pr_strength_prompt(prompt_params, prompt_params['neighborhood'])
        return result

    #
    async def _pr_strength_er_and_pr_prompt(self, prompt_params):
        result = await pr_strength_er_and_pr_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _pr_strength_zero_prompt(self, prompt_params):
        result = await pr_strength_zero_prompt(prompt_params, prompt_params['neighborhood'])
        return result

    #
    async def _pr_variability_prompt(self, prompt_params):
        result = await pr_variability_prompt(prompt_params, prompt_params['neighborhood'])
        return result

    #
    def _prompt_pr_percentage(self, prompt_params, full_neighborhood, bounded_neighborhood):
        regex = '([0-9]{1,2}|100)%'
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = {}
        if re.search(prompt_params['regex'],
                     full_neighborhood):
            if re.search('ER and PR', full_neighborhood):
                prompt_params['neighborhood'] = full_neighborhood
                prompt_params_trimmed = copy.deepcopy(prompt_params)
                trimmed_neighborhood = re.sub(' \- ([0-9]{1,2}|100)%', '', prompt_params['neighborhood'])
                prompt_params_trimmed['neighborhood'] = trimmed_neighborhood
                prompt_result = \
                    asyncio.run(self._pr_percentage_er_and_pr_prompt(prompt_params_trimmed))
            else:
                prompt_params['neighborhood'] = bounded_neighborhood
                prompt_params_trimmed = copy.deepcopy(prompt_params)
                trimmed_neighborhood = re.sub(' \- ([0-9]{1,2}|100)%', '', prompt_params['neighborhood'])
                prompt_params_trimmed['neighborhood'] = trimmed_neighborhood
                prompt_result = \
                    asyncio.run(self._pr_percentage_prompt(prompt_params_trimmed))
            result = [prompt_result.variables['CLS']]
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
            expansion_regex = {}
            expansion_regex['prefix'] = '((~|>|<) )?(([0-9]{1,2}|100)% \- )?'
            expansion_regex['suffix'] = '( \- ([0-9]{1,2}|100)%)?'
            result = \
                self._expand_result(expansion_regex, result, prompt_params['neighborhood'])
            if result is not None:
                for i in range(len(result)):
                    result[i] = re.sub(' \- ', '-', result[i])
        else:
            result = None
        return result

    #
    def _prompt_pr_score(self, prompt_params, full_neighborhood, bounded_neighborhood):
        regex = '[0-4](\+)?'
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = {}
        if re.search(prompt_params['regex'],
                     full_neighborhood):
            if re.search('ER and PR', full_neighborhood):
                prompt_params['neighborhood'] = full_neighborhood
                prompt_params_trimmed = copy.deepcopy(prompt_params)
                trimmed_neighborhood = re.sub(' \- [0-4](\+)?', '', full_neighborhood)
                prompt_params_trimmed['neighborhood'] = trimmed_neighborhood
                prompt_result = \
                    asyncio.run(self._pr_score_er_and_pr_prompt(prompt_params_trimmed))
            else:
                prompt_params['neighborhood'] = bounded_neighborhood
                prompt_params_trimmed = copy.deepcopy(prompt_params)
                trimmed_neighborhood = re.sub(' \- [0-4](\+)?', '', bounded_neighborhood)
                prompt_params_trimmed['neighborhood'] = trimmed_neighborhood
                prompt_result = \
                    asyncio.run(self._pr_score_prompt(prompt_params_trimmed))
            result = [prompt_result.variables['CLS']]
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
            expansion_regex = {}
            expansion_regex['prefix'] = '((~|>|<) )?'
            expansion_regex['suffix'] = '( \- [0-4](\+)?)?'
            result = \
                self._expand_result(expansion_regex, result, prompt_params['neighborhood'])
            if result is not None:
                for i in range(len(result)):
                    result[i] = re.sub(' \- ', '-', result[i])
        else:
            result = None
        return result

    #
    def _prompt_pr_staining(self, prompt_params, full_neighborhood, bounded_neighborhood):
        regex = '(?i)(favorable|negative|negativity|positive|positivity|unfavorable)'
        synonyms_dict = {}
        synonyms_dict['negative'] = ['negative', 'negativity']
        synonyms_dict['positive'] = ['positive', 'positivity']
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = synonyms_dict
        if re.search(prompt_params['regex'],
                     full_neighborhood):
            if re.search('ER and PR', full_neighborhood):
                prompt_params['neighborhood'] = full_neighborhood
                prompt_result = \
                    asyncio.run(self._pr_staining_er_and_pr_prompt(prompt_params))
            else:
                prompt_params['neighborhood'] = bounded_neighborhood
                prompt_result = \
                    asyncio.run(self._pr_staining_prompt(prompt_params))
            result = [prompt_result.variables['CLS']]
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
            expansion_regex = {}
            expansion_regex['prefix'] = \
                '(present and )?(very )?((diffusely|focally|low|minimally) )?'
            expansion_regex['suffix'] = None
            result = \
                self._expand_result(expansion_regex, result, prompt_params['neighborhood'])
            if result is not None:
                trimmed_result = []
                for i in range(len(result)):
                    if result[i].lower() != 'present and positive':
                        trimmed_result.append(result[i])
                result = trimmed_result
                if len(result) == 0:
                    result = None
        else:
            result = None
        return result

    #
    def _prompt_pr_strength(self, prompt_params, full_neighborhood, bounded_neighborhood):
        regex = '(?i)(moderate|no|strong|strongly|weak|weakly|zero)'
        synonyms_dict = {}
        synonyms_dict['strong'] = ['strong', 'strongly']
        synonyms_dict['weak'] = ['weak', 'weakly']
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = synonyms_dict
        if re.search(prompt_params['regex'],
                     full_neighborhood):
            result = []
            if re.search('(?i)(moderate|strong|strongly|weak|weakly)', prompt_params['neighborhood']):
                if re.search('ER and PR', full_neighborhood):
                    prompt_params['neighborhood'] = full_neighborhood
                    prompt_result = \
                        asyncio.run(self._pr_strength_er_and_pr_prompt(prompt_params))
                else:
                    prompt_params['neighborhood'] = bounded_neighborhood
                    prompt_result = \
                        asyncio.run(self._pr_strength_prompt(prompt_params))
                result.append(prompt_result.variables['CLS'])
            if re.search('(?i)(no|zero)', prompt_params['neighborhood']):
                prompt_result = \
                    asyncio.run(self._pr_strength_zero_prompt(prompt_params))
                result.append(prompt_result.variables['CLS'])
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
            expansion_regex = {}
            expansion_regex['prefix'] = '((very) )?((moderate|strong|weak) \- )?'
            expansion_regex['suffix'] = '( \- (moderate|strong|weak))?'
            result = \
                self._expand_result(expansion_regex, result, prompt_params['neighborhood'])
            if result is not None:
                for i in range(len(result)):
                    result[i] = re.sub(' \- ', '-', result[i])
                    result[i] = re.sub('(?i)no', 'none', result[i])
                    result[i] = re.sub('(?i)strongly', 'strong', result[i])
                    result[i] = re.sub('(?i)weakly', 'weak', result[i])
        else:
            result = None
        return result

    #
    def _prompt_pr_variability(self, prompt_params, neighborhood):
        regex = '(?i)variable'
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = {}
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'],
                     prompt_params['neighborhood']):
            prompt_result = \
                asyncio.run(self._pr_variability_prompt(prompt_params))
            result = [prompt_result.variables['CLS']]
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
        regex = self._get_limited_regex('PR')
        M = re.finditer(regex, text)
        if M:
            for m in M:
                full_neighborhood = \
                    self._get_full_neighborhood(text, m, regex, 50)
                bounded_neighborhood = \
                    self._get_bounded_neighborhood(text, m, regex,
                                                   self.prompt_params['radius'],
                                                   exclusion_dict)
                result = \
                    self._prompt_pr_percentage(self.prompt_params,
                                              full_neighborhood,
                                              bounded_neighborhood)
                results = self._extend_results(results, result, 'percentage')
                result = \
                    self._prompt_pr_score(self.prompt_params,
                                         full_neighborhood,
                                         bounded_neighborhood)
                results = self._extend_results(results, result, 'score')
                result = \
                    self._prompt_pr_staining(self.prompt_params,
                                            full_neighborhood,
                                            bounded_neighborhood)
                results = self._extend_results(results, result, 'staining')
                result = \
                    self._prompt_pr_strength(self.prompt_params,
                                            full_neighborhood,
                                            bounded_neighborhood)
                results = self._extend_results(results, result, 'strength')
                result = \
                    self._prompt_pr_variability(self.prompt_params,
                                               bounded_neighborhood)
                results = self._extend_results(results, result, 'variability')
            results = self._clean_results(results)
            results = self._get_superstrings(results, 'staining')
        if not bool(results):
            results = None
        return results