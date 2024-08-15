import requests
from bs4 import BeautifulSoup
import json

class MetaDataExtractor:

    def __init__(self, url):
        self.url = url
        self.soup = self._fetch_html()

    def _fetch_html(self):
        """Effettua una richiesta all'URL e ritorna il contenuto HTML analizzato da BeautifulSoup."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Verifica che la richiesta abbia avuto successo
            return BeautifulSoup(response.text, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f"Errore durante la richiesta HTTP: {e}")
            return None
        
    def get_meta_tag(self, name=None, property=None):
        """Estrae un singolo tag <meta> per nome o proprietà."""
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
    
    def get_title(self):
        """Estrae il titolo della pagina."""
        if not self.soup:
            return None
        title_tag = self.soup.title
        if title_tag:
            return title_tag.string
        return None
    
    def get_canonical_link(self):
        """Estrae il link canonico <link rel='canonical'>."""
        if not self.soup:
            return None
        canonical_tag = self.soup.find('link', attrs={'rel': 'canonical'})
        if canonical_tag and 'href' in canonical_tag.attrs:
            return canonical_tag['href']
        return None
    
    def extract_all_metadata(self):
        """Estrae tutti i metadati rilevanti e li restituisce come dizionario."""
        if not self.soup:
            return {}
        metadata = {
            'title': self.get_title(),
            'description': self.get_meta_tag(name='description'),
            'keywords': self.get_meta_tag(name='keywords'),
            'robots': self.get_meta_tag(name='robots'),
            'canonical': self.get_canonical_link(),
            'og:title': self.get_meta_tag(property='og:title'),
            'og:description': self.get_meta_tag(property='og:description'),
            'og:type': self.get_meta_tag(property='og:type'),
            'og:url': self.get_meta_tag(property='og:url'),
            'og:site_name': self.get_meta_tag(property='og:site_name'),
            'twitter:card': self.get_meta_tag(name='twitter:card'),
            'twitter:site': self.get_meta_tag(name='twitter:site'),
            'twitter:title': self.get_meta_tag(property='twitter:title'),
        }
        # Rimuove i metadati che non sono stati trovati (valori None)
        return {k: v for k, v in metadata.items() if v is not None}
    
    def to_json(self):
        """Restituisce i metadati estratti come stringa JSON."""
        metadata = self.extract_all_metadata()
        return json.dumps(metadata, ensure_ascii=False)

