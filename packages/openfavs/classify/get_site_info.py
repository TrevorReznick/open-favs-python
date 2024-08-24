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

    @staticmethod

    def is_excluded(word):
        if word is None:
            return True
        return Config.EXCLUDED_WORDS.get(word.lower().strip(), False)
    
class MetaDataExtractor:

    def __init__(self, url):

        self.url = url
        self.soup = self._fetch_html(url)
        #print('debug 1: ', self.url)

    def _fetch_html(self, url):

        try:
            response = requests.get(url)
            response.raise_for_status()  # Verifica che la richiesta abbia avuto successo
            return BeautifulSoup(response.text, 'html.parser')
        
        except requests.exceptions.RequestException as e:
            print(f"Errore durante la richiesta HTTP: {e}")
            return None
    def extract_all_metadata(self): 

        if not self.soup:
            return {}
        
        metadata = {
            
            'og:site_name': self.get_meta_tag(property='og:site_name'),
            'og:title': self.get_meta_tag(property='og:title'),
            'og:description': self.get_meta_tag(property='og:description'),
            'og:type': self.get_meta_tag(property='og:type'),
            'og:url': self.get_meta_tag(property='og:url'),
            'canonical': self.get_canonical_link(),
            'og:site_name': self.get_meta_tag(property='og:site_name'),
            'keywords': self.get_meta_tag(name='keywords')

        }
        
        return {k: v for k, v in metadata.items() if v is not None}
    
    def get_html_content(self):

        if not self.soup:
            print('debug, self soup: ', None)
            return None

        for element in self.soup(['nav', 'footer', 'header']):
            element.decompose()
            
        paragraphs = self.soup.find_all('p')
        all_text = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            all_text.append(text)
        
        if not all_text:

            print("Nessun testo trovato nei paragrafi.")
            return None
        
        # Restituisce una singola stringa che unisce tutti i paragrafi con una nuova linea tra di essi
        return "\n\n".join(all_text)   
    
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
    
    def get_name_by_host(self):
        url = self.url
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        
        # Lista dei sottodomini comuni da rimuovere
        common_subdomains = ['www', 'api', 'mail', 'ftp', 'blog', 'shop', 'dev', 'staging', 'test', 'm', 'cdn']

        # Rimozione dei sottodomini comuni
        for subdomain in common_subdomains:
            if hostname.startswith(f"{subdomain}."):
                hostname = hostname[len(subdomain) + 1:]
                break  # Rompe il ciclo dopo aver rimosso il primo sottodominio trovato
            
        # Split del dominio per ottenere la parte principale
        domain_parts = hostname.split('.')
        
        # Restituisce la prima parte del dominio, con la prima lettera maiuscola
        return domain_parts[0].capitalize()
    
    def get_name_by_host_old(self):
        url = self.url
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if hostname.startswith("www."):
            hostname = hostname[4:]            
            #print(hostname)
            domain_parts = hostname.split('.')
            return domain_parts[0].capitalize()
    
    # @@@ return object  @@@        
           
    
    def to_json(self):

        metadata = self.extract_all_metadata()
        content = self.get_html_content()

        filtered_metadata = {
            'name': None,
            'title': None,
            'description': None,
            'tags': None
        }

        # Itera sui metadati estratti
        for key, value in metadata.items():
            if Config.is_excluded(value):
                print(f"Il valore '{value}' per '{key}' è escluso.")
                continue

            # Controlla e assegna i valori
            if key == 'og:site_name':
                filtered_metadata['name'] = self.format_string(value)
            elif key == 'og:title':
                filtered_metadata['title'] = self.format_string(value)
            elif key == 'og:description':
                filtered_metadata['description'] = self.format_string(value)
            elif key == 'keywords':
                filtered_metadata['tags'] = value.split(', ')  # Splitta la stringa in una lista di tag

        # Gestisci fallback se i metadati non sono presenti
        if not filtered_metadata['name']:
            #url = metadata.get('canonical', '')
            filtered_metadata['name'] = self.get_name_by_host()            

        if not filtered_metadata['title']:
            alternate_title = self.get_title()
            filtered_metadata['title'] = alternate_title or 'Fallback Title'

        if not filtered_metadata['description']:
            alternate_description = self.get_description()
            print('alternate text')
            filtered_metadata['description'] = self.format_string(alternate_description) if alternate_description else 'Fallback Description'

        if not filtered_metadata['tags']:
            filtered_metadata['tags'] = []

        return json.dumps(filtered_metadata, ensure_ascii=False)
    
    def get_title(self):
    # Se soup non è definito, restituisce None
        if not self.soup:
            return None

        # Cerca il tag <title> o qualsiasi altro elemento con il tag 'title'
        title_tag = self.soup.title or self.soup.find('title')
        
        if title_tag:
            # Verifica se il titolo non è escluso e restituisce il testo formattato
            title_text = title_tag.get_text().strip()
            if not Config.is_excluded(title_text):
                return self.format_string(title_text)

        # Cerca un tag <h1> e verifica se il testo non è escluso
        h1_tag = self.soup.find('h1')
        if h1_tag:
            h1_text = h1_tag.get_text().strip()
            if not Config.is_excluded(h1_text):
                return h1_text

        # Cerca un tag <h2> e verifica se il testo non è escluso
        h2_tag = self.soup.find('h2')
        if h2_tag:
            h2_text = h2_tag.get_text().strip()
            if not Config.is_excluded(h2_text):
                return h2_text
        
        # Se c'è un titolo ma non è stato ancora formattato e restituito
        if title_tag and title_tag.string:
            return self.format_string(title_tag.string)
        
        # Se non viene trovato nulla di valido, restituisce None
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


