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
async def er_percentage_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: ER SP1 Carcinoma In Situ : Positive ( > = 1% )"
    "ANSWER: ER value is FALSE_POSITIVE\n"
    "EXAMPLE: ER ( 6F11 ) positive ( 2+ , > 80%\n"
    "ANSWER: ER value is 80%\n"
    "EXAMPLE: ER % invasive tumor cells staining : > 95%\n"
    "ANSWER: ER value is 95%\n"
    "EXAMPLE: ER strongly positive ( strong immunoreactivity in > 75%\n"
    "ANSWER: ER value is 75%\n"
    "EXAMPLE: ER % carcinoma in situ staining : 95%\n"
    "ANSWER: ER value is 95%\n"
    "EXAMPLE: ER ( SP1 ) Negative ( < 1%\n"
    "ANSWER: ER value is 1%\n"
    "EXAMPLE: ER ( SP1 ) Low Positive ( 2%\n"
    "ANSWER: ER value is 2%\n"
    "EXAMPLE: ER ( SP1 ) Positive ( 50%\n"
    "ANSWER: ER value is 50%\n"
    "EXAMPLE: ER ( SP1 ) Positive ( 80%\n"
    "ANSWER: ER value is 80%\n"
    "EXAMPLE: ER SP1 Positive > 95%\n"
    "ANSWER: ER value is 95%\n"
    "EXAMPLE: ER SP1 positive ( 100%\n"
    "ANSWER: ER value is 100%\n"
    "EXAMPLE: ER SP1 Positive 10%\n"
    "ANSWER: ER value is 10%\n"
    "EXAMPLE: 80% positivity for ER\n"
    "ANSWER: ER value is 80%\n"
    "EXAMPLE: ER 0%\n"
    "ANSWER: ER value is 0%\n"
    "EXAMPLE: ER 50%\n"
    "ANSWER: ER value is 50%\n"
    "EXAMPLE: ER 100%\n"
    "ANSWER: ER value is 100%\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: ER value is [CLS]\n" where STOPS_AT(CLS, '.') and REGEX(CLS, r"(?i)([0-9]{1,2}%|100%)")
    from prompt_params['lmql_model']
    '''

@lmql.query
async def er_score_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: ER ( 6F11 ) Positive 10% - 20% of DCIS , 2\n"
    "ANSWER: ER value is 2\n"
    "EXAMPLE: ER SP1 Positive > 95% of tumor cells , 2+\n"
    "ANSWER: ER value is 2+\n"
    "EXAMPLE: ER SP1 Positive 10% - 20% of DCIS , 2+\n"
    "ANSWER: ER value is 2+\n"
    "EXAMPLE: ER stain intensity ( carcinoma in situ ) : 3+\n"
    "ANSWER: ER value is 3+\n"
    "EXAMPLE: ER SP1 Positive > 95% of tumor , 3+\n"
    "ANSWER: ER value is 3+\n"
    "EXAMPLE: ER SP1 Positive > 95% of cells , 3+\n"
    "ANSWER: ER value is 3+\n"
    "EXAMPLE: ER ( SP1 ) positive ( 95% , 3+\n"
    "ANSWER: ER value is 3+\n"
    "EXAMPLE: ER SP1 Positive variable , ~ 10% 3+\n"
    "ANSWER: ER value is 3+\n"
    "EXAMPLE: ER ( SP1 ) negative ( 0\n"
    "ANSWER: ER value is 0\n"
    "EXAMPLE: ER ( 6F11 ) negative , 0+\n"
    "ANSWER: ER value is 0+\n"
    "EXAMPLE: ER ( 6F11 ) positive ( 2+\n"
    "ANSWER: ER value is 2+\n"
    "EXAMPLE: ER and PR ( 0 )\n"
    "ANSWER: ER value is 0\n"
    "EXAMPLE: ER ( > 80% 3\n"
    "ANSWER: ER value is 3\n"
    "EXAMPLE: 3 for PR\n"
    "ANSWER: PR value is 3\n"
    "EXAMPLE: ER SP1 1+\n"
    "ANSWER: ER value is 1+\n"
    "EXAMPLE: ER 1\n"
    "ANSWER: ER value is 1\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: ER value is [CLS]\n" where STOPS_AT(CLS, '.') and REGEX(CLS, r"(?i)[0-4](\+)?")
    from prompt_params['lmql_model']
    '''

@lmql.query
async def er_staining_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: ER SP1 Invasive Carcinoma : Positive\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: ER , and PR stains are negative\n"
    "ANSWER: ER value is negative\n"
    "EXAMPLE: ER ( SP1 ) Focally positive\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: ER ( SP1 ) Minimally positive\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: ER ( SP1 ) Weakly positive\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: ER ( 6F11 ) 2+ Positive\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: ER ( 6F11 ) Negative\n"
    "ANSWER: ER value is negative\n"
    "EXAMPLE: ER SP1 3+ Positive\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: ER strongly positive\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: ER SP1 Negative\n"
    "ANSWER: ER value is negative\n"
    "EXAMPLE: ER 98% Favorable\n"
    "ANSWER: ER value is favorable\n"
    "EXAMPLE: negative for ER\n"
    "ANSWER: ER value is negative\n"
    "EXAMPLE: positive for ER\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: negativity for ER\n"
    "ANSWER: ER value is negativity\n"
    "EXAMPLE: positivity for ER\n"
    "ANSWER: ER value is positivity\n"
    "EXAMPLE: ER is positive\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: ER favorable\n"
    "ANSWER: ER value is favorable\n"
    "EXAMPLE: ER negative\n"
    "ANSWER: ER value is negative\n"
    "EXAMPLE: ER positive\n"
    "ANSWER: ER value is positive\n"
    "EXAMPLE: ER unfavorable\n"
    "ANSWER: ER value is unfavorable\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: ER value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["favorable", "negative", "negativity", "positive", "positivity", "unfavorable"])
    from prompt_params['lmql_model']
    '''
    
@lmql.query
async def er_strength_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: ER ( 6F11 ) positive ( > 90% , strong\n"
    "ANSWER: ER value is strong\n"
    "EXAMPLE: ER SP1 Positive ( > 90% , moderate\n"
    "ANSWER: ER value is moderate\n"
    "EXAMPLE: ER is positive ( 100% , strong\n"
    "ANSWER: ER value is strong\n"
    "EXAMPLE: ER ( SP1 ) moderate\n"
    "ANSWER: ER value is moderate\n"
    "EXAMPLE: ER ( 6F11 ) Strongly\n"
    "ANSWER: ER value is strongly\n"
    "EXAMPLE: ER ( SP1 ) Weakly\n"
    "ANSWER: ER value is weakly\n"
    "EXAMPLE: strongly diffusely positive for ER\n"
    "ANSWER: ER value is strongly\n"
    "EXAMPLE: strong diffusely positive ER\n"
    "ANSWER: ER value is strong\n"
    "EXAMPLE: ER SP1 weak\n"
    "ANSWER: ER value is weak\n"
    "EXAMPLE: strongly positive for ER\n"
    "ANSWER: ER value is strongly\n"
    "EXAMPLE: ER moderate\n"
    "ANSWER: ER value is moderate\n"
    "EXAMPLE: ER strong\n"
    "ANSWER: ER value is strong\n"
    "EXAMPLE: ER strongly\n"
    "ANSWER: ER value is strongly\n"
    "EXAMPLE: ER weak\n"
    "ANSWER: ER value is weak\n"
    "EXAMPLE: ER weakly\n"
    "ANSWER: ER value is weakly\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n"where STOPS_AT(REASON, '.') 
    "ANSWER: ER value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["moderate", "strong", "strongly", "weak", "weakly"])
    from prompt_params['lmql_model']
    '''
    
@lmql.query
async def er_strength_zero_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: ER ( SP1 ) Negative ( No\n"
    "ANSWER: ER value is no\n"
    "EXAMPLE: ER 6F11 Negative zero\n"
    "ANSWER: ER value is zero\n"
    "EXAMPLE: ER zero\n"
    "ANSWER: ER value is zero\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n"where STOPS_AT(REASON, '.')
    "ANSWER: ER value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["no", "zero"])
    from prompt_params['lmql_model']
    '''
    
@lmql.query
async def er_variability_prompt(prompt_params, neighborhood):
    '''lmql
    argmax(max_len=prompt_params['max_len'])
    "[[INST]]Classify the text using the given examples. Explain your reasoning.[[/INST]]\n"
    "EXAMPLE: ER ( SP1 ) Focally positive ( variable\n"
    "ANSWER: ER value is variable\n"
    "EXAMPLE: ER ( 6F11 ) positive ( variable\n"
    "ANSWER: ER value is variable\n"
    "EXAMPLE: ER ( SP11 ) variable\n"
    "ANSWER: ER value is variable\n"
    "EXAMPLE: ER variable\n"
    "ANSWER: ER value is variable\n"
    "EXAMPLE: variable ER\n"
    "ANSWER: ER value is variable\n"
    "EXAMPLE: PR ( 1E2 ) positive ( variable\n"
    "ANSWER: ER value is FALSE_POSITIVE\n"
    "TEXT: {neighborhood}\n"
    "REASONING: [REASON]\n" where STOPS_AT(REASON, '.') 
    "ANSWER: ER value is [CLS]\n" where STOPS_AT(CLS, '.') and CLS in set(["variable"])
    from prompt_params['lmql_model']
    '''

#
class Er_prompts_object(prompts_base_object):
    
    #
    async def _er_percentage_prompt(self, prompt_params):
        result = await er_percentage_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _er_score_prompt(self, prompt_params):
        result = await er_score_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _er_staining_prompt(self, prompt_params):
        result = await er_staining_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _er_strength_prompt(self, prompt_params):
        result = await er_strength_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _er_strength_zero_prompt(self, prompt_params):
        result = await er_strength_zero_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    async def _er_variability_prompt(self, prompt_params):
        result = await er_variability_prompt(prompt_params, prompt_params['neighborhood'])
        return result
    
    #
    def _prompt_er_percentage(self, prompt_params, neighborhood):
        regex = '([0-9]{1,2}|100)%'
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = {}
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'],
                     prompt_params['neighborhood']):
            prompt_params_trimmed = copy.deepcopy(prompt_params)
            trimmed_neighborhood = re.sub(' \- ([0-9]{1,2}|100)%', '', neighborhood)
            prompt_params_trimmed['neighborhood'] = trimmed_neighborhood
            prompt_result = \
                asyncio.run(self._er_percentage_prompt(prompt_params_trimmed))
            result = [ prompt_result.variables['CLS'] ]
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
            expansion_regex = {}
            expansion_regex['prefix'] = '((~|>|<) )?(([0-9]{1,2}|100)% \- )?'
            expansion_regex['suffix'] = '( \- ([0-9]{1,2}|100)%)?'
            result = \
                self._expand_result(expansion_regex, result, neighborhood)
            if result is not None:
                for i in range(len(result)):
                    result[i] = re.sub(' \- ', '-', result[i])
        else:
            result = None
        return result
    
    #
    def _prompt_er_score(self, prompt_params, neighborhood):
        regex = '[0-4](\+)?'
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = {}
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'],
                     prompt_params['neighborhood']):
            prompt_params_trimmed = copy.deepcopy(prompt_params)
            trimmed_neighborhood = re.sub(' \- [0-4](\+)?', '', neighborhood)
            prompt_params_trimmed['neighborhood'] = trimmed_neighborhood
            prompt_result = \
                asyncio.run(self._er_score_prompt(prompt_params_trimmed))
            result = [ prompt_result.variables['CLS'] ]
            result = \
                self._clean_result(prompt_params['regex'], result)
            result = \
                self._confirm_result(prompt_params['neighborhood'],
                                     prompt_params['synonyms_dict'], result)
            expansion_regex = {}
            expansion_regex['prefix'] = '((~|>|<) )?'
            expansion_regex['suffix'] = '( \- [0-4](\+)?)?'
            result = \
                self._expand_result(expansion_regex, result, neighborhood)
            if result is not None:
                for i in range(len(result)):
                    result[i] = re.sub(' \- ', '-', result[i])
        else:
            result = None
        return result
    
    #
    def _prompt_er_staining(self, prompt_params, neighborhood):
        regex = '(?i)(favorable|negative|negativity|positive|positivity|unfavorable)'
        synonyms_dict = {}
        synonyms_dict['negative'] = [ 'negative', 'negativity' ]
        synonyms_dict['positive'] = [ 'positive', 'positivity' ]
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = synonyms_dict
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'],
                     prompt_params['neighborhood']):
            prompt_result = \
                asyncio.run(self._er_staining_prompt(prompt_params))
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
                self._expand_result(expansion_regex, result, neighborhood)
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
    def _prompt_er_strength(self, prompt_params, neighborhood):
        regex = '(?i)(moderate|no|strong|strongly|weak|weakly|zero)'
        synonyms_dict = {}
        synonyms_dict['strong'] = [ 'strong', 'strongly' ]
        synonyms_dict['weak'] = [ 'weak', 'weakly' ]
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = synonyms_dict
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'],
                     prompt_params['neighborhood']):
            result = []
            if re.search('(?i)(moderate|strong|strongly|weak|weakly)', prompt_params['neighborhood']):
                prompt_result = \
                    asyncio.run(self._er_strength_prompt(prompt_params))
                result.append(prompt_result.variables['CLS'])
            if re.search('(?i)(no|zero)', prompt_params['neighborhood']):
                prompt_result = \
                    asyncio.run(self._er_strength_zero_prompt(prompt_params))
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
                self._expand_result(expansion_regex, result, neighborhood)
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
    def _prompt_er_variability(self, prompt_params, neighborhood):
        regex = '(?i)variable'
        prompt_params['regex'] = regex
        prompt_params['synonyms_dict'] = {}
        prompt_params['neighborhood'] = neighborhood
        if re.search(prompt_params['regex'],
                     prompt_params['neighborhood']):
            prompt_result = \
                asyncio.run(self._er_variability_prompt(prompt_params))
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
        regex = self._get_limited_regex('ER')
        M = re.finditer(regex, text)
        if M:
            for m in M:
                neighborhood = \
                    self._get_bounded_neighborhood(text, m, regex,
                                                   self.prompt_params['radius'],
                                                   exclusion_dict)
                result = self._prompt_er_percentage(self.prompt_params, neighborhood)
                results = self._extend_results(results, result, 'percentage')
                result = self._prompt_er_score(self.prompt_params, neighborhood)
                results = self._extend_results(results, result, 'score')
                result = self._prompt_er_staining(self.prompt_params, neighborhood)
                results = self._extend_results(results, result, 'staining')
                result = self._prompt_er_strength(self.prompt_params, neighborhood)
                results = self._extend_results(results, result, 'strength')
                result = self._prompt_er_variability(self.prompt_params, neighborhood)
                results = self._extend_results(results, result, 'variability')
            results = self._clean_results(results)
            results = self._get_superstrings(results, 'staining')
        if not bool(results):
            results = None
        return results