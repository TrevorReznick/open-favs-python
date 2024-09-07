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
        

def process_tags(stringa):
    # Dividi la stringa per '&' per ottenere le coppie chiave=valore
    pairs = stringa.split('&')
    obj = {}

    for pair in pairs:
        key, value = pair.split('=')
        key = key.strip()
        value = value.strip().strip('"')  # Rimuovi eventuali spazi e virgolette attorno ai valori

        # Controlla se la chiave è tag_2 per separare ulteriormente id e category
        if key == 'tag_2':
            if ':' in value:  # Verifica se il valore contiene 'id:category'
                id_value, category = value.split(':', 1)
                obj[key] = {'id': id_value, 'category': category}
            else:
                obj[key] = {'category': value}  # Caso di fallback se non c'è ':'

        # Controlla se la chiave è tag_3, tag_4, o tag_5 per separare ulteriormente id e sub_category
        elif key in ['tag_3', 'tag_4', 'tag_5']:
            if ':' in value:  # Verifica se il valore contiene 'id:sub_category'
                id_value, sub_category = value.split(':', 1)
                obj[key] = {'id': id_value, 'sub_category': sub_category}
            else:
                obj[key] = {'sub_category': value}  # Caso di fallback se non c'è ':'
        else:
            obj[key] = value  # Aggiungi la coppia key-value per altri tag normalmente

    return obj

def process_tags_old(stringa):
    # Dividi la stringa per '&' per ottenere le coppie chiave=valore
    pairs = stringa.split('&')
    obj = {}

    for pair in pairs:
        key, value = pair.split('=')
        key = key.strip()
        value = value.strip().strip('"')  # Rimuovi eventuali spazi e virgolette attorno ai valori

        # Controlla se la chiave è tag_3, tag_4, o tag_5 per separare ulteriormente id e sub_category
        if key in ['tag_2', 'tag_3', 'tag_4', 'tag_5']:
            if ':' in value:  # Verifica se il valore contiene 'id:testo'
                id_value, sub_category = value.split(':', 1)
                obj[key] = {'id': id_value, 'sub_category': sub_category}
            else:
                obj[key] = {'sub_category': value}  # Caso di fallback se non c'è ':'
        else:
            obj[key] = value  # Aggiungi la coppia key-value per altri tag normalmente

    return obj

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

def get_complex_obj(object):
    
    obj = {}

    for item in object:
        area = item['area']
        categoria = item['category']
        sotto_categorie = [{'id': sub['id'], 'sub_category': sub['sub_category']} for sub in item['sub_categories']]

        if area not in obj:
            obj[area] = {}

        if categoria not in obj[area]:
            obj[area][categoria] = []

        obj[area][categoria].extend(sotto_categorie)

    return obj




