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

class KeyPop():
    def __init__(self):
        self.df = pd.read_excel( '../data/output/2_keywords_popularity.xlsx')
        self.df.set_index( "keyword", inplace=True)
        df_sorted = self.df.sort_values( "article_count", ascending=True).head(100)
        mean_values = df_sorted.mean()
        
        self.unknown_min = int( mean_values.min_shares)
        self.unknown_max = int( mean_values.max_shares)
        self.unknown_avg = int( mean_values.avg_shares)

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
            
        for keyword in key_list:
            key = keyword.strip()
            
            min_shares = self.unknown_min
            max_shares = self.unknown_max
            avg_shares = self.unknown_avg
            
            if self.df.index.contains(key):
                min_shares = self.df.at[key, "min_shares"]
                max_shares = self.df.at[key, "max_shares"]
                avg_shares = self.df.at[key, "avg_shares"]
    
            #total_shares += (((max_shares - min_shares) / 2) + \
            #                        avg_shares) / 2
            total_shares += avg_shares
            
        if len(key_list) > 0:
            total_shares = int( total_shares / len(key_list))
        
        return total_shares