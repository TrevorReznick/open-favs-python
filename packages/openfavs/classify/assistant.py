
import get_site_info

class Config:
    MODEL = "gpt-35-turbo"
    START_PAGE = ""
    WELCOME = "Benenuti nell'assistente virtuale di Openfavs"
    ROLE = """
        You are an data entry analist of this site. You should have to classify a bookmark site
        after you grab the default information.
    """
    EMAIL = "enzonav@yahoo.it"
    THANKS = ""
    ERROR = ""
    OUT_OF_SERVICE = ""
    INAPPROPRIATE = ""

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
        self.ai =  AzureOpenAI(api_version="2023-12-01-preview", 
                               api_key=self.key, 
                               azure_endpoint=self.host
                            )
        
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
            response = requests.get(url)
            #soup = BeautifulSoup(response.text, 'html.parser')       
            #title = soup.title.string
            extractor = get_site_info.MetaDataExtractor(url)
            json_metadata = extractor.to_json()
            metadata_dict = json.loads(json_metadata)
            #titolo = metadata_dict.get('og:title')
            #self.add_element('title', titolo)
            #descrizione = metadata_dict.get('og:description')
            #self.add_element('description', descrizione)
            #print(json_metadata)
            #return self.site_info
            #return json_metadata
            return metadata_dict
            """
            title_tag = soup.find('title')
            meta_description = soup.find('meta', attrs={"name": "description"})
            description = soup.title.description
            
            self.add_element('description', description)
            print("Debug Titolo:", title)
            print('Debug title_tag: ', title_tag)
            print('Debug meta_description: ', meta_description)
            print('Debug description: ', description)
            """

    """
    def test(self, args):
        url = args.get("url", "none")
        greeting = "url: " + url + "!"
        #print(greeting)
        return greeting
    """      
        

AI = None
Web = None

def main(args):

    global AI, Web

    print('into main')

    if AI is None: AI = ChatBot(args)    
    if Web is None: Web = Website(args)

    return {"body": Web.get_request(args)}
