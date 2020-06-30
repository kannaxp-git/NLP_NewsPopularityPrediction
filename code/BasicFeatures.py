# -*- coding: utf-8 -*-
"""
BasicFeatures.py

Usage:
    from BasicFeatures import BasicFeaturesCreator as bfc
    
    result = bfc.get_basic_features( html_doc)
    
    each value can be got by,
    result.fieldname
        n_tokens_title
        n_tokens_content
        n_unique_tokens
        n_non_stop_words
        n_non_stop_unique_tokens
        num_hrefs
        num_self_hrefs
        num_imgs
        num_videos
        average_token_length
        num_keywords
        data_channel_is_lifestyle
        data_channel_is_entertainment
        data_channel_is_bus
        data_channel_is_socmed
        data_channel_is_tech
        data_channel_is_world

@author: vnithiya
"""

import re

# For NLP actions
from bs4 import BeautifulSoup
from bs4 import element

import spacy
nlp = spacy.load('en_core_web_sm')

from collections import Counter

class BasicFeatures():
    def __init__(self):
        self.n_tokens_title = 0
        self.n_tokens_content = 0
        self.n_unique_tokens = 0.0
        self.n_non_stop_words = 0.0
        self.n_non_stop_unique_tokens = 0.0
        self.num_hrefs = 0
        self.num_self_hrefs = 0
        self.num_imgs = 0
        self.num_videos = 0
        self.average_token_length = 0.0
        self.num_keywords = 0
        self.data_channel_is_lifestyle = 0
        self.data_channel_is_entertainment = 0
        self.data_channel_is_bus = 0
        self.data_channel_is_socmed = 0
        self.data_channel_is_tech = 0
        self.data_channel_is_world = 0

class BasicFeaturesCreator():
    def __init__(self):
        pass
    
    def get_basic_features(html_doc):
        return_object = BasicFeatures()
        
        soup = BeautifulSoup(html_doc, 'html.parser')
        
        title = ""
        if not soup.title == None:
            title = str( soup.title.string)
        nlp_title = nlp(title)
        
        n_tokens_title = 0
        for token in nlp_title:
            n_tokens_title += 1

        # the contents containing repeating / unnecessary info - these classes are excluded
        exclude_class_list = [ "top-stories-promo-story__summary"]
        
        exclude_starts_with = ["Additional reporting by"]
        regex_keyword = """<meta content="(?P<keyword1>[^><\/\"]*)"\s[a-zA-Z="\-]*\sname="keywords".?.?>"""
        
        content = "" # soup.title.string + "\n"
        
        num_hrefs = 0
        num_self_hrefs = 0
        num_imgs = 0
        num_videos = 0
        
        for p in soup.select( "p"):
            for child in p.children:
                if isinstance( child, element.Tag):
                    if not child.name is None:
                        if child.name == "a":
                            num_hrefs += 1
                            
                            href_url = child.get('href')
                            if (not href_url is None) and ("mashable.com" in href_url.lower()):
                                num_self_hrefs += 1
                                
                        if child.name == "img" or child.name == "picture":
                            num_imgs += 1
                            
                        if child.name == "iframe":
                            if "youtube.com" in str( child.get("src")):
                                num_videos += 1
                            
            text = p.get_text()
        
            if len( text.split()) > 1:
                if text not in content:
                    is_in_exclude_list = False
        
                    for exclude_class in exclude_class_list:
                        if p.has_attr("class") and \
                            exclude_class in p.get_attribute_list( "class"):
        
                            is_in_exclude_list = True
                            break
        
                    for starts_string in exclude_starts_with: 
                        if text.startswith(starts_string):
                            is_in_exclude_list = True
                            break
        
                    if not is_in_exclude_list:
                        content = content + text + "\n"

        nlp_content = nlp(content)
        
        tokens = [token.text for token in nlp_content]
                        #if not token.is_stop and not token.is_punct]
        
        n_tokens_content = len(tokens)
        
        if n_tokens_content == 0:
            n_tokens_content = 1

        average_token_length = 0
        for token in tokens:
            average_token_length += len(token)
        
        average_token_length = average_token_length / n_tokens_content
        
        count_unique_tokens = len( Counter(tokens))
        if count_unique_tokens == 0:
            count_unique_tokens = 1
        
        n_unique_tokens = len( Counter(tokens)) / n_tokens_content
        
        tokens = [token.text for token in nlp_content if not token.is_stop and not token.is_punct]
        
        n_non_stop_words = len(tokens) / n_tokens_content

        n_non_stop_unique_tokens = len( Counter(tokens)) / count_unique_tokens

        # Keywords
        regex_keyword = """<meta content="(?P<keyword1>[^><\/\"]*)"\s[a-zA-Z="\-]*\sname="keywords".?.?>"""
        
        keywords = ""
        
        for meta in soup.find_all( 'meta'):
            meta_text = str(meta)
            match = re.search( regex_keyword, meta_text)
            if match:
                if not match.group("keyword1") == None:
                    keywords = match.group("keyword1")
                    break
                    
        # if keywords is not found, take non-stop words from title
        if keywords == "":
            tokens = [token.text for token in nlp_title if not token.is_stop and not token.is_punct]
            keywords = ", ".join( tokens)

        num_keywords = len( keywords.split(", "))

        # Data channel
        data_channel = ""
        for p in soup.select( "hgroup"):
            if not p.get("data-channel") == None:
                data_channel = p.get("data-channel")
                
        data_channel = data_channel.lower()
        
        data_channel_is_lifestyle = 1 if data_channel == "culture" or data_channel == "" else 0
        data_channel_is_entertainment = 1 if data_channel == "entertainment" else 0
        data_channel_is_bus = 1 if data_channel == "business" else 0
        data_channel_is_socmed = 1 if data_channel == "social-good" else 0
        data_channel_is_tech = 1 if data_channel == "tech" else 0
        data_channel_is_world = 1 if data_channel == "world" or data_channel == "u.s." else 0
        
        return_object.n_tokens_title = n_tokens_title
        return_object.n_tokens_content = n_tokens_content
        return_object.n_unique_tokens = n_unique_tokens
        return_object.n_non_stop_words = n_non_stop_words
        return_object.n_non_stop_unique_tokens = n_non_stop_unique_tokens
        return_object.num_hrefs = num_hrefs
        return_object.num_self_hrefs = num_self_hrefs
        return_object.num_imgs = num_imgs
        return_object.num_videos = num_videos
        return_object.average_token_length = average_token_length
        return_object.num_keywords = num_keywords
        return_object.data_channel_is_lifestyle = data_channel_is_lifestyle
        return_object.data_channel_is_entertainment = data_channel_is_entertainment
        return_object.data_channel_is_bus = data_channel_is_bus
        return_object.data_channel_is_socmed = data_channel_is_socmed
        return_object.data_channel_is_tech = data_channel_is_tech
        return_object.data_channel_is_world = data_channel_is_world
        
        return return_object
