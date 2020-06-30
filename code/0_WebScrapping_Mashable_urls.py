# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 03:40:45 2020

@author: kach
"""

#import required libraries
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


def get_title(soup):
    return soup.title.text

def get_content(soup):
    key_content=soup.find_all(class_='article-content')
    content=''
    for txt in key_content:
        content=content+txt.get_text()+' '
    
    return content


if __name__=='__main__':
    df=pd.read_excel('../data/input/OnlineNewsPopularity.xlsx')
    df=df[['Id','url']]
    
    df['title']=''
    df['content']=''
    
    for index,row in df.iterrows():
        print(index,row.url)
        
        #exit condition
        #if index>3:
        #    break
        
        try:
            html_content = requests.get(row.url).text
            soup = BeautifulSoup(html_content, "html.parser")
            
            title=get_title(soup)
            content=get_content(soup)
            
            df.loc[index,'title']=title
            df.loc[index,'content']=content

            #source file
            text_file = open("../data/output/html/"+ str(index+1)+".html", "w",encoding="utf-8")
            text_file.write(str(soup))
            text_file.close()
            
            #atricle content
            text_file = open("../data/output/txt/"+ str(index+1)+".txt", "w",encoding="utf-8")
            text_file.write(content)
            text_file.close()
            

        except:
            df.loc[index,'title']=''
            df.loc[index,'content']=''


#writing df
df.to_excel('../data/output/SS_Extracted_content.xlsx',index=False)
df.to_csv('../data/output/SS_Extracted_content.txt',sep='\t',index=False)