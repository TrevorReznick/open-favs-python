import requests
from urllib.parse import urlparse
import re
import socket

class MetadataProcessingError(Exception):
    
    """Eccezione personalizzata per la gestione degli errori di elaborazione dei metadati."""
    
    pass

class WebControl:

    def __init__(self, url):
        
        self.url = url
        self.parsed_url = urlparse(url)
        
    def validate_site(self):
        
        error_log = {}
        
        access_logs = {}
        
        _functions = {
            
            "valid_url": self.is_valid_url,
            "accessible" : self.is_accessible,
            "secure" : self.is_secure,
            "domain_exists": self.domain_exists,
            "redirect_exists": self.get_redirects,
            "html_content_exists": self.get_html_content,
            "status_code": self.status_code
        
        }
        
        for key, func in _functions.items():
            
            try:
                # Applica la funzione di processing alla chiave
                access_logs[key] = func()
                
            except MetadataProcessingError as e:
                # Registra l'errore per la chiave specifica
                error_log[key] = str(e)
                
            except Exception as e:
                # Registra errori generici non previsti
                error_log[key] = f"Errore sconosciuto: {str(e)}"

        # Se ci sono errori, ritorna un dizionario di errori e una risposta 5XX
        
        if error_log:
            return {
                "body": error_log
            }
        else:
            return {
                "body": access_logs
            }
            
    def is_valid_url(self):

        # Verifica la validità dell'URL
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// o https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # dominio...
            r'localhost|'  # ...o localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...o un indirizzo IPv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...o un indirizzo IPv6
            r'(?::\d+)?'  # porta opzionale
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if re.match(regex, self.url) is None:
            #raise MetadataProcessingError(f"Errore: URL non valido - '{self.url}'")
            return None
        
        return re.match(regex, self.url) is not None

    def status_code(self):
        
        # Verifica se l'URL è accessibile e restituisce un codice di stato 200
        try:
            response = requests.head(self.url, allow_redirects=True, timeout=5)
            
            return response.status_code
        
        except requests.exceptions.RequestException:
            
            raise MetadataProcessingError("Errore generico!")
    
    def is_accessible(self):

        # Verifica se l'URL è accessibile e restituisce un codice di stato 200
        try:
            response = requests.head(self.url, allow_redirects=True, timeout=5)
            
            if response.status_code == 200:
                
                return True
        
        except requests.exceptions.RequestException:
            
            raise MetadataProcessingError(f"Errore: URL non valido - '{self.url}'")
            

    def is_secure(self):

        # Verifica se l'URL utilizza HTTPS
        return self.parsed_url.scheme == 'https'

    def domain_exists(self):

        # Verifica se il dominio dell'URL esiste
        try:
            domain = self.parsed_url.netloc
            socket.gethostbyname(domain)
            return True
        
        except socket.error:
            raise MetadataProcessingError(f"Errore: dominio non esistente - '{domain}'")

    def get_redirects(self):

        # Verifica se l'URL reindirizza e restituisce l'URL finale
        try:
            response = requests.head(self.url, allow_redirects=True, timeout=5)
            
            return True if response.url != self.url else None
        
        except requests.exceptions.RequestException:
            return None

    def get_html_content(self):

        # Estrae il contenuto HTML della pagina
        try:
            response = requests.get(self.url, timeout=5)
            
            if response.status_code == 200:
                return True
            else:
                return None
        
        except requests.exceptions.RequestException:
            
            raise MetadataProcessingError(f"Html status code: {response.status_code}")
            

    def get_url_info(self):

        # Esegui tutti i controlli e restituisci i risultati
        results = {
            "is_valid_url": self.is_valid_url(),
            "is_accessible": self.is_accessible(),
            "is_secure": self.is_secure(),
            "domain_exists": self.domain_exists(),
            "redirects_to": self.get_redirects(),
            "html_content": self.get_html_content()
        }
        return results
    
    def validate_url(self):
        # Esegui tutti i controlli e restituisci i risultati
        if self.is_valid_url():
            return self.url
        else:
            print("Invalid URL")
            return None

"""
    Esempio di utilizzo
    url = "https://www.example.com"
    web_control = WebControl(url)
    results = web_control.test()

    print("Risultati del Controllo:")
    for check, result in results.items():
        print(f"{check}: {result}")
"""