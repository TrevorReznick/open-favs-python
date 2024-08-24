
#import packages.openfavs.classify.get_site_info_old as get_site_info_old
from openai import AzureOpenAI, BadRequestError
import get_site_info, web_control
from load_json import main_cat, sub_cat
from utils import find_partial_matches, find_partial_matches_new, split_sentence, create_phrases_dict

class Config:
    MODEL = "gpt-4"
    WELCOME = "Benenuti nell'assistente virtuale di Openfavs"
    #ROLE = "You are the Openfavs virtual assistant. The first answear to first input have to be: 'hello, i'm an Openfavs assistant. How can help you? "
    ROLE = "You are the Openfavs virtual assistant, your role is web site analyst, classifyng the input data"   
    GEMERIC_ROLE = "You are a generic GPT-4 assistant, provide kindly answers to user's questions"
    ERROR = "There was an error processing your request"
    OUT_OF_SERVICE = "We apogize, but the assistant is not available. Coming soon"
    INAPPROPRIATE = "Temo che la tua richiesta possa essere fraintesa. Puoi riformularla in maniera più appropriata?"
    SUGGESTIONS = {
        "cloud-native": "serverless",
        "portfolio": "inspiration",
        "projects": "inspiration",
        "full stack developer": "developement",
        "amministratore di sisteme": "system engineer"
    }


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

    # @@ get the cats json object @@ #

    main_cat_str = ", ".join([f"{item['cat_name']}" for item in main_cat])
    sub_cat_str = ", ".join([f"{item['cat_name']}" for item in sub_cat])     
    
    description = extractor.get_description()
    html_content = extractor.get_html_content()

    #
    if(description):
        print('description exists :', description)
    else: 
        print('description not exists!')

    # @@ testing find similarities and spli sentences @@ #

    """matches = find_partial_matches(description, Config.SUGGESTIONS)

    for match in matches:
        print(f"Found match: {match[0]} -> {match[1]}")
    """

    # 1. Suddividi la frase in sottofrasi
    sub_phrases = split_sentence(description)
    print(f"Sub-phrases: {sub_phrases}")

    # 2. Crea un dizionario delle sottofrasi
    phrases_dict = create_phrases_dict(sub_phrases)
    print(f"Phrases dictionary: {phrases_dict}")

    suggestions_found = {}
    suggestion = ""


    
    for idx, sub_phrase in phrases_dict.items():

        matches = find_partial_matches_new(sub_phrase, Config.SUGGESTIONS)

        formatted_matches = [{k: v} for k, v in matches]

        if formatted_matches:  # Aggiungi solo se ci sono match
            suggestion_ = suggestions_found[sub_phrase] = formatted_matches
            suggestion_1 = [list(d.values())[0] for d in suggestion_]
            #print('suggestion', suggestion)
            suggestion = (" ".join(suggestion_1))
            print('suggestion', suggestion)
        else:
            print('nessuna suggestion trovata')


        """if(matches):
            print(f"Matches for sub-phrase '{sub_phrase}': {matches}")
        else:
            print('nessuna suggestion trovata')"""
    
    # @@ prod flow @@ #

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
        You should be so skilled to identify the main_category one solely by from the choosing list: {main_cat_str} analizyng the description: {description} 
        and if there is suggestion {suggestion} give it as main_category; furthermore, you should find 5 tags exclusively from the list:  {sub_cat_str} 
        and classify the site you are analizyng by providing 5 classify tags; the tags in the list should already be exhaustive for the classification 
        we intend to do, but only if you cannot find tags adaptable to the description, then you will suggest new tags, using the formula: suggested tags - > tags, 
        inserting them separately in the list of results of which you will find the formatting rules later.
        I please you to split the strict answer question, the classification, and notes of the logic you have used using the following rules: use a json object with 
        this shape: 
        {{
            'main_category': category, 
            '(your)tag_1': your_tag_1, 
            'your_tag_2': your_tag_2, 
            'your_tag_3': your_tag_3, 
            'your_tag_4': your_tag_4,
            'your_tag_5': your_tag_5,
            ***'suggested_tag_n': suggested_tag_n***
        }};
        the response will be a string without spaces, prefixed with str_to_obj: the json_object_string, a string of the notes of logic prefixed with 'my_string: ""'
        thanks a lot!        
    """
    request_old = f"""
        You should be so skilled to identify the main_category one solely by from the choosing list: {main_cat_str} analizyng the description: {description};
        furthermore, you should find 5 tags exclusively from the list:  {sub_cat_str} and classify the site you are analizyng by providing 5 classify tags.
        There are 2 based data strings, main category: {main_cat_str} and sub category: {sub_cat_str}, a description {description}, a site content: {html_content} 
        and a suggestion {suggestion} for main category; can you give me 1 main category, consider suggestion if present and 5 sub category tags, 
        from provided strings within the description? if description has not suitable informations, you will consider the whole site content provided? 
        I please you to split the strict answer question, classification, parsed in markdown, and enventual notes of the logic you have used; 
        last part is optional. Thanks a lot!
    """
    #print('prompt', request)
    classify = AI.asks_ai(request, Config.ROLE)
    # Step 2: Assicurati che classify sia una stringa
        
    json_match = re.search(r'str_to_obj:({.*?})', classify)
    if json_match:
        json_str = json_match.group(1)
        try:
            # Converti la stringa JSON in un dizionario Python
            json_data = json.loads(json_str)
            formatted_json = json.dumps(json_data, indent=4)
            print("Contenuto JSON estratto e formattato:")
            print(formatted_json)
        except json.JSONDecodeError as e:
            print(f"Errore nel decodificare la stringa JSON: {e}")
    else:
        print("Nessun contenuto JSON trovato.")

    # Estrarre il contenuto di my_string
    my_string_match = re.search(r'my_string:"([^"]*)"', classify)
    if my_string_match:
        AI_analysis = my_string_match.group(1)
        print("\nContenuto di my_string:")
        print(AI_analysis)
    else:
        print("Nessun contenuto my_string trovato.")

    # Step 4: Controlla se la stringa è vuota
    """
    if not classify_str:
        print("La risposta di AI.asks_ai è vuota o contiene solo spazi.")
        AI_response = None
    else:
        try:
            # Step 5: Converte la stringa in un dizionario Python
            AI_response = json.loads(classify_str)

            # Step 6: Formatta e stampa il dizionario come JSON formattato
            formatted_json = json.dumps(AI_response, indent=4)
            print(formatted_json)

        except json.JSONDecodeError as e:
            print(f"Errore nel decodificare la stringa JSON: {e}")
            print(f"Contenuto ricevuto: '{classify_str}'")  # Debug: stampa il contenuto per capire il problema
            AI_response = None
    """       
            
    
    
    
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

     
