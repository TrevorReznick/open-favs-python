import logging, requests, re, json
from urllib.parse import urlparse
from bs4 import BeautifulSoup

from urllib.parse import urlparse
from utils import format_string

class MetaDataExtractor:
    def __init__(self, url):      
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Definisci l'URL e ottieni l'HTML
        self.url = url
        self.soup = self.fetch_html(url)

    def fetch_html(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Errore durante la richiesta HTTP: {e}")
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

    def extract_metadata(self):
        metadata = Config.METADATA_NEW.copy()

        def safe_extract(key, extraction_function):
            try:
                if callable(extraction_function):
                    value = extraction_function()
                    if value is not None and not Config.is_excluded(value):
                        metadata[key] = value
                    else:
                        self.logger.info(f"Il valore per '{key}' è nullo o escluso.")
                else:
                    self.logger.warning(f"Funzione di estrazione per '{key}' non valida.")
            except Exception as e:
                self.logger.error(f"Errore nell'estrazione di '{key}': {str(e)}")

        # Estrazione dei metadati Open Graph
        og_properties = {
            'name': 'og:site_name',
            'title': 'og:title',
            'description': 'og:description',
            'canonical': 'og:canonical',
            'url': 'og:url',
            'type': 'og:type',
            'image': 'og:image',
        }

        for key, property in og_properties.items():
            safe_extract(key, lambda: self.get_meta_tag(property=property))

        # Estrazione di metadati aggiuntivi
        safe_extract('domain', lambda: self.get_meta_tag(property='forem:domain'))
        safe_extract('logo', lambda: self.get_meta_tag(property='forem:logo'))

        # Fallback per titolo e descrizione
        if metadata['title'] is None:
            safe_extract('title', lambda: self.get_meta_tag(name='title'))
        if metadata['description'] is None:
            safe_extract('description', lambda: self.get_meta_tag(name='description'))

        # Funzioni di fallback personalizzate
        fallback_functions = {
            "name": self.get_name_by_host,
            "title": self.get_title,
            "description": self.get_description,
            "canonical": self.get_canonical_link,
            "url": lambda: self.url
        }

        for key, fallback_function in fallback_functions.items():
            if metadata[key] is None:
                safe_extract(key, fallback_function)

        # Rimuovi i valori None dal dizionario
        metadata = {k: v for k, v in metadata.items() if v is not None}

        self.logger.info("Estrazione dei metadati completata.")
        return json.dumps(metadata, ensure_ascii=False)

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
                return format_string(text)
        return None

    def get_name_by_host(self):
        parsed_url = urlparse(self.url)
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

    def get_html_content(self):
        if not self.soup:
            self.logger.warning('Debug, self.soup is None')
            return None

        for element in self.soup(['nav', 'footer', 'header']):
            element.decompose()
            
        paragraphs = self.soup.find_all('p')
        all_text = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            all_text.append(text)
        
        if not all_text:
            self.logger.warning("Nessun testo trovato nei paragrafi.")
            return None
        
        return "\n\n".join(all_text)

# Assicurati che la classe Config sia definita correttamente
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

    @staticmethod
    def is_excluded(word):
        if word is None:
            return True
        return Config.EXCLUDED_WORDS.get(word.lower().strip(), False)
