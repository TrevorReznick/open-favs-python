
#import packages.openfavs.classify.get_site_info_old as get_site_info_old
from openai import AzureOpenAI, BadRequestError
import get_site_info
from load_json import main_cat, sub_cat

class Config:
    MODEL = "gpt-35-turbo"
    WELCOME = "Benenuti nell'assistente virtuale di Openfavs"
    ROLE = "You are the Openfavs virtual assistant. The first answear to first input have to be: 'hello, i'm an Openfavs assistant. How can help you? "   
    ERROR = "There was an error processing your request"
    OUT_OF_SERVICE = "We apogize, but the assistant is not available. Coming son"
    INAPPROPRIATE = "Temo che la tua richiesta possa essere fraintesa. Puoi riformularla in maniera più appropriata?"
    
    
    


import re, json, os
import requests
from openai import AzureOpenAI, BadRequestError
from bs4 import BeautifulSoup
#import traceback, random
#from html_sanitizer import Sanitizer
#from urllib.parse import urlparse
#from difflib import SequenceMatcher


class ChatBot:

    def __init__(self, args):

        print('init class chatbot')
        OPENAI_API_KEY = '89773db3-7863-460c-ad3c-6abd0db43f1c'
        OPENAI_API_HOST = 'https://openai.nuvolaris.io'
        print('init chatbot()')        
        self.key = OPENAI_API_KEY
        self.host = OPENAI_API_HOST
        self.ai =  AzureOpenAI(
            api_version="2023-12-01-preview", 
            api_key=self.key, 
            azure_endpoint=self.host
        )

    def test(self, input, role):

        print('asking chatbot')

        req = [ 
            {"role": "system", "content": role}, 
            {"role": "user", "content": input}
        ]

        try:
            comp = self.ai.chat.completions.create(model=Config.MODEL, messages=req)
            if len(comp.choices) > 0:
                content = comp.choices[0].message.content
                return content
            
        except BadRequestError as e:            
            return Config.INAPPROPRIATE
        
        except Exception as e:
            return Config.OUT_OF_SERVICE
        return None
        
        
class Website:

    def __init__(self, args):

        self.response = ""
        self.site_info = {}
        #self.sanitizer = Sanitizer()  
        print('init class website')    
    
    def add_element(self, element, value):

        # Aggiunge una coppia chiave-valore al dizionario
        self.site_info[element] = value
        return self.site_info
    
    
    def get_request(self, args):
        url = args.get("url")
        if url:
            extractor = get_site_info.MetaDataExtractor(url)
            json_metadata = extractor.to_json()
            metadata_obj = json.loads(json_metadata)            
            return metadata_obj

AI = None
Web = None

def main(args):

    global AI, Web

    print('into main')

    if AI is None: AI = ChatBot(args)    
    if Web is None: Web = Website(args)

    print('test load json')
    #print(main_cat)
    #print(sub_cat)    
    request = "If i give you an object,and a content site, you can try to give me 3 tags from the object to classify the site?"
    chat_gpt = AI.test(request, Config.ROLE)
    print(chat_gpt)
    return {"body": Web.get_request(args)}

"""
title_tag = soup.find('title')
meta_description = soup.find('meta', attrs={"name": "description"})
description = soup.title.description
self.add_element('description', description)
#self.add_element('meta_description' , meta_description)
print("Debug Titolo:", title)
print('Debug title_tag: ', title_tag)
#print('Debug meta_description: ', meta_description)
if meta_description:
    print(meta_description['content'])  # Stampa il contenuto del tag meta description
    # Estrai il canonical link
    canonical_link = soup.find('link', attrs={'rel': 'canonical'})
    if canonical_link:
        print(canonical_link['href'])  # Stampa l'URL del canonical link
        tag_as_string = str(canonical_link)
        json_output = json.dumps({'content': tag_as_string}, ensure_ascii=False)
        self.add_element('canonical_link', json_output)
    # Estrai i metadati og:title
    #og_title = soup.find('meta', attrs={'property': 'og:title'})
    #if og_title:
    #print(og_title['content'])  # Stampa il contenuto del tag og:title
    #self.add_element('og_title', og_title)
    print('Debug description: ', description)
    return self.site_info
"""

     
