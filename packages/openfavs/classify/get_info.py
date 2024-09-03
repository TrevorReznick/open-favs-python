import requests
from bs4 import BeautifulSoup
import re, json
from urllib.parse import urlparse
from utils import format_string

class Config:

    EXCLUDED_WORDS = {
        "homepage": True,
        "default": True,
        "dashboard": True,
        "untitled": True,
        "null": False,
        "undefined": True,
        "index": True,
        "benvenuto": True,
        "sezioni": True,
        "": True,
        None: False
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
        'logo': None,
        'icon': None,
        'author': None
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
    
    def extract_metadata(self): #prende i metadata e restituisce oggetto solo se valori non sono nulli

        metadata = Config.METADATA_NEW        
        
        # @@ get graph metatags @@ 
        
        metadata['name'] = self.get_meta_tag(property='og:site_name')
        metadata['title'] =  self.get_meta_tag(property='og:title')
        metadata['description'] = self.get_meta_tag(property='og:description')
        metadata['url'] = self.get_meta_tag(property='og:url')
        metadata['type'] = self.get_meta_tag(property='og:type')
        metadata['image'] = self.get_meta_tag(property='og:image')        
        metadata['domain'] = self.get_meta_tag(property='forem:domain')
        metadata['logo'] = self.get_meta_tag(property='forem:logo')

        # @@ get name metatag @@
        
        if metadata['title'] is None:

            metadata['title'] = self.get_meta_tag(name='title')

        if metadata['description'] is None:

            metadata['description'] = self.get_meta_tag(name='description')
        
        
        print('metadata: ', metadata)

        # Dizionario per associare le chiavi alle funzioni specifiche
        _functions = {

            "name": self.get_name_by_host,
            "title": self.get_title,
            "description": self.get_description,
            "url": lambda: "hello from missing description"           

        }

        for key, value in metadata.items():

            if value is None:

                print(f"'{key}': is None")                

                if key in _functions:

                    value = _functions[key]()

                    Config.METADATA_NEW[key] = value

                    continue
            else:
                
                if Config.is_excluded(value):
                    
                    print(f"Il valore '{value}' per '{key}' è escluso.")

                    if key in _functions:

                        print('printing from existent value')

                        value = _functions[key]()

                        Config.METADATA_NEW[key] = value

                continue

            print('new metadata: ', Config.METADATA_NEW)

            return
    
    def get_description(self):        
        if not self.soup:
            return None        
        paragraphs = self.soup.find_all('p')
        for p in paragraphs:
            text = p.get_text().strip()
            if not Config.is_excluded(text):
                return format_string(text)            
        return None
    
    def get_name_by_host(self):
        url = self.url
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname        
        common_subdomains = ['www', 'api', 'mail', 'ftp', 'blog', 'shop', 'dev', 'staging', 'test', 'm', 'cdn']        
        for subdomain in common_subdomains:
            if hostname.startswith(f"{subdomain}."):
                hostname = hostname[len(subdomain) + 1:]
                break        
        domain_parts = hostname.split('.')        
        return domain_parts[0].capitalize()
    
    def get_title(self):
        if not self.soup:            
            return None
        title_tag = self.soup.title or self.soup.find('title')        
        if title_tag:            
            title_text = title_tag.get_text().strip()
            if not Config.is_excluded(title_text):
                return format_string(title_text)        
        h1_tag = self.soup.find('h1')
        if h1_tag:
            h1_text = h1_tag.get_text().strip()
            if not Config.is_excluded(h1_text):
                return h1_text
        h2_tag = self.soup.find('h2')
        if h2_tag:
            h2_text = h2_tag.get_text().strip()
            if not Config.is_excluded(h2_text):
                return h2_text        
        if title_tag and title_tag.string:
            return format_string(title_tag.string)        
        return None
    
    
    