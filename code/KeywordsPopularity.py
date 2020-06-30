# -*- coding: utf-8 -*-
"""
KeywordsPopularity.py

Keywords Popularity based shares prediction

call as follows
==================
from KeywordsPopularity import KeyPop

keyPop = KeyPop()

keyPop.predict_shares( comma_separated_string_with_keywords or a list of keywords)

returns expected shares prediction
=================

@author: vnithiya
"""

import pandas as pd

class KeywordPredictionsResult():
    def __init__(self):
        self.avg_avg = 0
        self.min_avg = 0
        self.max_avg = 0
        self.avg_avg_no_clip = 0
        self.min_avg_no_clip = 0
        self.max_avg_no_clip = 0

class KeyPop():
    def __init__(self):
        self.df = pd.read_excel( '../data/output/2_keywords_popularity.xlsx')
        self.df.set_index( "keyword", inplace=True)
        df_sorted = self.df.sort_values( "article_count", ascending=True).head(100)
        mean_values = df_sorted.mean()
        
        self.unknown_min = int( mean_values.min_shares)
        self.unknown_max = int( mean_values.max_shares)
        self.unknown_avg = int( mean_values.avg_shares)

        self.unknown_min_no_clip = int( mean_values.min_shares_no_clip)
        self.unknown_max_no_clip = int( mean_values.max_shares_no_clip)
        self.unknown_avg_no_clip = int( mean_values.avg_shares_no_clip)
        
    def predict_shares(self, keywords):
        '''
        predicts shares based on the given keywords. taken comma separated string or list of keywords
        
        for each keywords checks avg_shares
        
        takes average of all the keywords
        
        For unknown keywords - keywords not in the list uses mean_values of bottom 100 least used keywords
        '''
        key_list = keywords
        if isinstance(key_list, str):
            key_list = key_list.split(",")
            
        total_shares = 0
        total_shares_no_clip = 0
        
        min_avg_shares = 1000000
        min_avg_shares_no_clip = 1000000
            
        max_avg_shares = 0
        max_avg_shares_no_clip = 0
        
        for keyword in key_list:
            key = keyword.strip()
            
            avg_shares = self.unknown_avg
            avg_shares_no_clip = self.unknown_avg_no_clip
            
            if self.df.index.contains(key):
                avg_shares = self.df.at[key, "avg_shares"]
                avg_shares_no_clip = self.df.at[key, "avg_shares_no_clip"]
    
            total_shares += avg_shares
            total_shares_no_clip += avg_shares_no_clip
            
            if avg_shares < min_avg_shares:
                min_avg_shares = avg_shares
            
            if avg_shares_no_clip < min_avg_shares_no_clip:
                min_avg_shares_no_clip = avg_shares_no_clip
                
            if avg_shares > max_avg_shares:
                max_avg_shares = avg_shares
            
            if avg_shares_no_clip > max_avg_shares_no_clip:
                max_avg_shares_no_clip = avg_shares_no_clip
                
        avg_avg_shares = 0
        avg_avg_shares_no_clip = 0
        
        if len(key_list) > 0:
            avg_avg_shares = int( total_shares / len(key_list))
            avg_avg_shares_no_clip = int( total_shares_no_clip / len(key_list))
            
        result = KeywordPredictionsResult()
        result.avg_avg = avg_avg_shares
        result.max_avg = max_avg_shares
        result.min_avg = min_avg_shares
        result.avg_avg_no_clip = avg_avg_shares_no_clip
        result.max_avg_no_clip = max_avg_shares_no_clip
        result.min_avg_no_clip = min_avg_shares_no_clip
        
        return result