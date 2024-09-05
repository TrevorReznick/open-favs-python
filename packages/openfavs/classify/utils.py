import re, json
from difflib import SequenceMatcher

def format_string(input_string):
        
        if input_string is None:
            return None
        try:
            # Rimuove eventuali spazi vuoti indesiderati
            return input_string.strip()
        
        except AttributeError as e:
            print(f"Errore durante la formattazione della stringa: {e}")
            return input_string.strip()
        

def parse_string_to_dict(s):
    # Dividi la stringa per il segno '&' per ottenere coppie chiave-valore
    pairs = s.split('&')
    result = {}
    
    for pair in pairs:
        # Dividi la coppia per '=' per ottenere la chiave e il valore
        key, value = pair.split('=', 1)
        # Rimuovi i doppi apici dal valore
        value = value.strip('"')
        # Aggiungi la coppia chiave-valore al dizionario
        result[key] = value
    
    return result


