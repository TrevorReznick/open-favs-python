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

    METADATA = {
        'name': None,
        'title': None,
        'description': None,
        'canonical': None,
        'keywords': None,
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
        
    def get_meta_tag(self, name=None, property=None, charset=False):

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
    
    def medatata_extractor(self):

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
    
    """
    def no_metadata(self):
        # Fallback per il titolo
        if not Config.METADATA['title']:
            Config.METADATA['title'] = self.get_title() or "Titolo predefinito"
        
        # Fallback per la descrizione
        if not Config.METADATA['description']:
            Config.METADATA['description'] = "Descrizione predefinita"
        
       
        
        # Aggiungi altri fallback secondo necessita
    """
    
    
    def extract_metadata(self): 

        if not self.soup:
            return {}
        
        self.medatata_extractor()
        
        metadata = Config.METADATA            
        
        filtered_metadata = {k: v for k, v in metadata.items() if v is not None}
        
        if not filtered_metadata:
            return None
        
        return filtered_metadata
    
    
    