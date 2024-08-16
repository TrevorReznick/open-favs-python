import requests
from bs4 import BeautifulSoup
import json

class Config:

    EXCLUDED_WORDS = {
        "homepage": True,
        "default": True,
        "untitled": True,
        "null": True,
        "undefined": True,
        "index": True,
        "": True,
        None: True,
    }

    @staticmethod
    def is_excluded(word):
        if word is None:
            return True
        return Config.EXCLUDED_WORDS.get(word.lower().strip(), False)
    
class MetaDataExtractor:

    def __init__(self, url):
        self.url = url
        self.soup = self._fetch_html()

    def _fetch_html(self):

        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Verifica che la richiesta abbia avuto successo
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Errore durante la richiesta HTTP: {e}")
            return None
        
    def get_meta_tag(self, name=None, property=None):

        if not self.soup:
            return None
        
        if name:
            tag = self.soup.find('meta', attrs={'name': name})

        elif property:
            tag = self.soup.find('meta', attrs={'property': property})

        else:
            return None

        if tag and 'content' in tag.attrs:
            return tag['content']
        
        return None
    
    # @@@ refactoring @@@    
    
    
    def get_title(self):
        
        if not self.soup:
            return None
        
        title_tag = self.soup.title

        if title_tag and not Config.is_excluded(title_tag.get_text()):
            return title_tag.get_text().strip()
        
        h1_tag = self.soup.find('h1')

        if h1_tag and not Config.is_excluded(h1_tag.get_text()):
            return h1_tag.get_text().strip()
        
        h2_tag = self.soup.find('h2')

        if h2_tag and not Config.is_excluded(h2_tag.get_text()):
            return h2_tag.get_text().strip()
        
        title_tag = self.soup.find('title')

        if title_tag and title_tag.string:
            print(title_tag)
            return self.format_string(title_tag.string)
        
        return None
    
    def get_canonical_link(self):

        if not self.soup:
            return None
        
        canonical_tag = self.soup.find('link', attrs={'rel': 'canonical'})

        if canonical_tag and 'href' in canonical_tag.attrs:
            return canonical_tag['href']
        
        return None
    
    def get_description(self):
        
        if not self.soup:
            return None
        
        paragraphs = self.soup.find_all('p')

        for p in paragraphs:
            text = p.get_text().strip()
            if not Config.is_excluded(text):
                return self.format_string(text)
            
        return None
    
    def format_string(self, input_string):
        
        if input_string is None:
            return None
        try:
            # Rimuove eventuali spazi vuoti indesiderati
            return input_string.strip()
        except AttributeError as e:
            print(f"Errore durante la formattazione della stringa: {e}")
            return input_string.strip()
    
    def extract_all_metadata(self):        
        if not self.soup:
            return {}
        metadata = {
            
            'og:title': self.get_meta_tag(property='og:title'),
            'og:description': self.get_meta_tag(property='og:description'),
            'og:type': self.get_meta_tag(property='og:type'),
            'og:url': self.get_meta_tag(property='og:url'),
            'canonical': self.get_canonical_link(),
            'og:site_name': self.get_meta_tag(property='og:site_name'),
            'keywords': self.get_meta_tag(name='keywords')

        }
        
        return {k: v for k, v in metadata.items() if v is not None}         
    
    def to_json(self):

        metadata = self.extract_all_metadata()

        filtered_metadata = {}

        for key, value in metadata.items():
            if Config.is_excluded(value):
                print(f"Il valore '{value}' per '{key}' è escluso.")
                continue

            filtered_metadata[key] = self.format_string(value)
        
        # Se nessun metadato valido è trovato, usa fallback nel contenuto della pagina
        if not filtered_metadata:
            
            print("Nessun metadato valido trovato, si passa al fallback...")

            alternate_title = self.get_title()

            if alternate_title:
                filtered_metadata['title'] = alternate_title

            # Fallback per descrizione
            alternate_description = self.get_description()

            if alternate_description:
                filtered_metadata['description'] = self.format_string(alternate_description)

        return json.dumps(filtered_metadata, ensure_ascii=False)
    
    
"""
metadata = {
    'title': self.get_title(),
    'description': self.get_meta_tag(name='description'),
    'canonical': self.get_canonical_link(),
    'keywords': self.get_meta_tag(name='keywords'),
    'robots': self.get_meta_tag(name='robots'),            
    'og:title': self.get_meta_tag(property='og:title'),
    'og:email': self.get_meta_tag(property='og:email'),
    'og:description': self.get_meta_tag(property='og:description'),
    'og:type': self.get_meta_tag(property='og:type'),
    'og:url': self.get_meta_tag(property='og:url'),
    'og:site_name': self.get_meta_tag(property='og:site_name'),
    'twitter:card': self.get_meta_tag(name='twitter:card'),
    'twitter:site': self.get_meta_tag(name='twitter:site'),
    'twitter:title': self.get_meta_tag(property='twitter:title'),
}
"""


