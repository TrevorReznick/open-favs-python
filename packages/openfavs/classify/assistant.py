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
#from bs4 import BeautifulSoup
#import traceback, random
#from html_sanitizer import Sanitizer
#from urllib.parse import urlparse
#from difflib import SequenceMatcher

class ChatBot:

    def __init__(self, args):
        print('init chatbot()')
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
        print('init website()')
        

    def test(self, args):
        url = args.get("url", "none")
        greeting = "url: " + url + "!"
        print(greeting)
        return greeting
        #return {"body": greeting}
        #response = {"body": greeting}
        #return greeting
        

AI = None
Web = None

def main(args):

    global AI, Web

    print('into main')

    if AI is None: AI = ChatBot(args)    
    if Web is None: Web = Website(args)
    return {"body": Web.test(args)}
    # test args
    #url = args.get("url", "none")
    #greeting = "url: " + url + "!"
    # return {"body": greeting}
    #response = {"body": greeting}
    #return #greeting