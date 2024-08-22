
#import packages.openfavs.classify.get_site_info_old as get_site_info_old
from openai import AzureOpenAI, BadRequestError
import get_site_info, web_control
from load_json import main_cat, sub_cat
from utils import find_partial_matches

class Config:
    MODEL = "gpt-4"
    WELCOME = "Benenuti nell'assistente virtuale di Openfavs"
    #ROLE = "You are the Openfavs virtual assistant. The first answear to first input have to be: 'hello, i'm an Openfavs assistant. How can help you? "
    ROLE = "You are the Openfavs virtual assistant, your role is web site analyst, classifyng the input data"   
    GEMERIC_ROLE = "You are a generic GPT-4 assistant, provide kindly answers to user's questions"
    ERROR = "There was an error processing your request"
    OUT_OF_SERVICE = "We apogize, but the assistant is not available. Coming soon"
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

        #print('init class chatbot')
        OPENAI_API_KEY = '89773db3-7863-460c-ad3c-6abd0db43f1c'
        OPENAI_API_HOST = 'https://openai.nuvolaris.io'      
        self.key = OPENAI_API_KEY
        self.host = OPENAI_API_HOST
        self.ai =  AzureOpenAI(
            api_version="2023-12-01-preview", 
            api_key=self.key, 
            azure_endpoint=self.host
        )

    def asks_ai(self, input, role):

        print('asking chatbot')
        #print('input', input)
        #print('role', role)

        req = [ 
            {"role": "system", "content": role}, 
            {"role": "user", "content": input}
        ]

        try:
            comp = self.ai.chat.completions.create(model=Config.MODEL, messages=req)
            if len(comp.choices) > 0:
                content = comp.choices[0].message.content
                #print('debug chatbot')
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
        self.url = args.get("url")  
        #print('debug assistant', args)
        #self.sanitizer = Sanitizer()  
        #print('init class website')    
    

    def get_request(self, args):        
        self.url = args.get("url")  
        #url_control = web_control.WebControl(self, args)
        #print(url_control.get_url_info())
        extractor = get_site_info.MetaDataExtractor(args.get("url"))
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
    
    url = args.get("url")
    print('init MetaDataExtractor class')
    extractor = get_site_info.MetaDataExtractor(url)

    main_cat_str = ", ".join([f"{item['cat_name']}" for item in main_cat])
    sub_cat_str = ", ".join([f"{item['cat_name']}" for item in sub_cat])     
    
    description = extractor.get_description()
    html_content = extractor.get_html_content()
    print('debug :', description)

    # qui viene seguito controllo se la pagina è accessibile o meno

    if(html_content):
        print('html content found!')

    else:
        url_utils = web_control.WebControl(url)
        url_logs = url_utils.get_url_info()
        print('html content not found; ', url_logs)
        print('debug html content found: ', url_utils.get_html_content())
        print('debug soup results: ', extractor.get_html_content())
    #print(html_content)
    #request = f"If I give you an object with categories {main_cat_str} and {sub_cat_str}, and a content site, can you give me 3 tags from the object to classify the site?"
    request = f"""
        There are 2 based data strings, main category: {main_cat_str} and sub category: {sub_cat_str}, a description {description} and a site content: {html_content}; 
        can you give me 1 main category tag and 5 sub category tags, from provided strings and the he description; if description has not suitable inormations, you will consider the whole site content provided? I please you
        to split the strict answer question, classification, parsed in markdown, and enventual notes of the logic you have used; last part is optional?
    """
    #print('prompt', request)
    classify = AI.asks_ai(request, Config.ROLE)
    print(classify)
    request_1 = "Oh, you are so precious; could you provide from the strict answer a json object with the object = main_cat main_cat: your_main_cat_tag_answer, sub_cat_tag_1: your_sub_cat_tag_answer_1, ..."
    re_classify = AI.asks_ai(request_1, Config.ROLE)   
    print(re_classify)
    return {
        "body": Web.get_request(args)
    }

"""
def add_element(self, element, value):
    # Aggiunge una coppia chiave-valore al dizionario
    self.site_info[element] = value
    return self.site_info

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

     
