import requests
from bs4 import BeautifulSoup
import re, json
from urllib.parse import urlparse

class Config:

    EXCLUDED_WORDS = {
        "homepage": True,
        "default": True,
        "dashboard": True,
        "untitled": True,
        "null": True,
        "undefined": True,
        "index": True,
        "Benvenuto": True,
        "sezioni": True,
        "": True,
        None: True,
    }

    METADATA_NEW = {
        'name': None,
        'title': None,
        'description': None,
        'type': None,
        'url': None, 
        'image': None,
        'canonical': None,
        'keywords': None,
        'domain': None,
        'logo': None
    }
    
    METADATA = {
                
        
        'robots': None,
        'og:title': None,
        'og:description': None,
        'og:type': None,
        'og:url': None,
        'og:site_name': None,
        'og:image': None,
        'og:image:alt': None,
        'twitter:card': None,
        'twitter:site': None,
        'twitter:title': None,
        'twitter:image': None,
        'apple-touch-icon': None,
        'icon': None,
        'author': None,
        'viewport': None,
        'charset': None
    }


    @staticmethod

    def is_excluded(word):
        if word is None:
            return True
        return Config.EXCLUDED_WORDS.get(word.lower().strip(), False)
    
class MetaDataExtractorNew:

    def __init__(self, url):

        self.url = url
        self.soup = self.fetch_html(url)
        #print('debug 1: ', self.url)

    def fetch_html(self, url):

        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica che la richiesta abbia avuto successo
            return BeautifulSoup(response.text, 'html.parser')
        
        except requests.exceptions.RequestException as e:
            print(f"Errore durante la richiesta HTTP: {e}")
            return None
        
    def get_meta_tag(self, name=None, property=None, charset=False): # utity function prende i metadati in base agli argomenti

        if not self.soup:
            return None
        
        if name:
            tag = self.soup.find('meta', attrs={'name': name})

        elif property:
            tag = self.soup.find('meta', attrs={'property': property})

        elif charset:
            tag = self.soup.find('meta', attrs={'charset': True})

        else:
            return None

        if tag and 'content' in tag.attrs:
            return tag['content']
        
        if charset and tag:
            return tag.get('charset')
        
        return None
    
    def medatata_extractor_old(self): #analizza il contenuto del sito e popola oggetto metadata        

        
        for key in Config.METADATA:
            
            if key.startswith('og:'):
                Config.METADATA[key] = self.get_meta_tag(property=key)              
                                
            elif key.startswith('twitter:'):
                Config.METADATA[key] = self.get_meta_tag(property=key)
                
            else:
                # Gestione speciale per 'charset'
                if key == 'charset':
                    Config.METADATA[key] = self.get_meta_tag(charset=True)
                else:
                    # Cerca per 'name' e non 'property'
                    Config.METADATA[key] = self.get_meta_tag(name=key)

        return
    
    
    
    
    def extract_metadata(self): #prende i metadata e restituisce oggetto solo se valori non sono nulli

        metadata = Config.METADATA_NEW     
        
        metadata['name'] = self.get_meta_tag(property='og:site_name')
        metadata['title'] =  self.get_meta_tag(property='og:title')
        metadata['description'] = self.get_meta_tag(property='og:description')
        metadata['url'] = self.get_meta_tag(property='og:url')
        metadata['type'] = self.get_meta_tag(property='og:type')
        metadata['image'] = self.get_meta_tag(property='og:image')        
        metadata['domain'] = self.get_meta_tag(property='forem:domain')
        metadata['logo'] = self.get_meta_tag(property='forem:logo')
        
        
        my_filtered_metadata = {
            k: v for k, v in metadata.items() if v is not None
        }
        
        if not my_filtered_metadata:
            return None 
        
        for key, value in metadata.items():
            if value is None:
                print(f"La proprietà '{key}' ha un valore None.")     
        
        
        return my_filtered_metadata
    
    
    