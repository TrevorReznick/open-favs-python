import re, json
from difflib import SequenceMatcher 

def extract_json(output, prefix):
    """
    Estrae un oggetto JSON basato su un prefisso specificato.

    :param output: La stringa di input contenente il JSON.
    :param prefix: Il prefisso usato per identificare l'oggetto JSON nella stringa.
    :return: Un dizionario contenente 'json_data' se trovato.
    """
    # Crea un pattern dinamico per l'oggetto JSON
    json_pattern = rf'{prefix}:({{.*?}})'
    
    # Trova e decodifica il JSON
    json_match = re.search(json_pattern, output)
    if json_match:
        json_str = json_match.group(1)
        try:
            json_data = json.loads(json_str)
            formatted_json = json.dumps(json_data, indent=4)
            print("Contenuto JSON estratto e formattato:")
            print(formatted_json)
            return {'json_data': json_data}
        except json.JSONDecodeError as e:
            print(f"Errore nel decodificare la stringa JSON: {e}")
            return {'json_data': None}
    else:
        print("Nessun contenuto JSON trovato.")
        return {'json_data': None}

def extract_my_string(output, prefix):
    """
    Estrae il contenuto di 'my_string' basato su un prefisso specificato.

    :param output: La stringa di input contenente la stringa di analisi.
    :param prefix: Il prefisso usato per identificare la stringa di analisi nella stringa.
    :return: Un dizionario contenente 'AI_analysis' se trovato.
    """
    # Crea un pattern dinamico per la stringa di analisi
    analysis_pattern = rf'{prefix}:"([^"]*)"'
    analysis_match = re.search(analysis_pattern, output)
    if analysis_match:
        AI_analysis = analysis_match.group(1)
        print("\nContenuto di my_string:")
        print(AI_analysis)
        return {'AI_analysis': AI_analysis}
    else:
        print("Nessun contenuto my_string trovato.")
        return {'AI_analysis': None}    
    


def find_partial_matches_old(input_phrase, dictionary, threshold=0.8):
        matches = []
        words = input_phrase.split()
        for key, value in dictionary.items():
            for word in words:
                if word in key:
                    matches.append((key, value))
                else:
                    similarity = SequenceMatcher(None, word, key).ratio()
                    if similarity >= threshold:
                        matches.append((key, value))
        return matches

def split_sentence(sentence):
    # Usa una regex per separare la frase su ', ', ' and ', ';' e altri separatori
    sub_phrases = re.split(r',\s*|and\s+|;\s*|\.\s*|\b e \b', sentence)
    # Rimuovi spazi bianchi inutili e stringhe vuote
    sub_phrases = [phrase.strip() for phrase in sub_phrases if phrase.strip()]
    return sub_phrases

def create_phrases_dict(sub_phrases):
    # Crea un dizionario dove la chiave è l'indice e il valore è la sottofrase
    phrases_dict = {i: sub_phrase for i, sub_phrase in enumerate(sub_phrases)}
    return phrases_dict

def find_partial_matches_new(input_phrase, dictionary, threshold=0.8):
    matches = []
    words = set(input_phrase.split())
    
    for key, value in dictionary.items():
        key_words = set(key.split())
        
        if not key_words.issubset(words):
            continue
        
        similarity_full_phrase = SequenceMatcher(None, input_phrase, key).ratio()
        
        if similarity_full_phrase >= threshold:
            matches.append((key, value))
            continue
        
        for word in words:
            similarity = SequenceMatcher(None, word, key).ratio()
            if similarity >= threshold:
                matches.append((key, value))
                break
    
    matches = list(set(matches))
    matches.sort(key=lambda x: SequenceMatcher(None, input_phrase, x[0]).ratio(), reverse=True)
    
    return matches

def find_partial_matches(input_phrase, dictionary, threshold=0.8):
    matches = []
    words = set(input_phrase.split())
    print(f"Input phrase words: {words}")  # Debug: Mostra le parole nella frase di input

    for key, value in dictionary.items():
        key_words = set(key.split())
        print(f"Checking key: '{key}' with words: {key_words}")  # Debug: Mostra la chiave e le sue parole
        
        # Verifica che tutte le parole della chiave siano presenti nella descrizione
        if not key_words.issubset(words):
            print(f"Key '{key}' does not match because not all words are present in the description.")
            continue  # Salta se la chiave contiene parole non presenti nella description
        
        # Controlla l'intera frase rispetto alla chiave
        similarity_full_phrase = SequenceMatcher(None, input_phrase, key).ratio()
        print(f"Similarity with full phrase for key '{key}': {similarity_full_phrase}")  # Debug: Similarità con la frase intera
        
        if similarity_full_phrase >= threshold:
            print(f"Key '{key}' matches with full phrase (similarity: {similarity_full_phrase})")
            matches.append((key, value))
            continue
        
        # Controlla ogni parola separatamente
        for word in words:
            similarity = SequenceMatcher(None, word, key).ratio()
            print(f"Similarity with word '{word}' for key '{key}': {similarity}")  # Debug: Similarità con ogni parola
            if similarity >= threshold:
                print(f"Key '{key}' matches with word '{word}' (similarity: {similarity})")
                matches.append((key, value))
                break  # Evita duplicati aggiuntivi
    
    # Rimuove duplicati e ordina per similarità se necessario
    matches = list(set(matches))
    matches.sort(key=lambda x: SequenceMatcher(None, input_phrase, x[0]).ratio(), reverse=True)
    
    print(f"Final matches: {matches}")  # Debug: Mostra i risultati finali
    return matches

def find_partial_matches_old1(input_phrase, dictionary, threshold=0.8):

    matches = []
    words = input_phrase.split()
    
    for key, value in dictionary.items():
        # Controlla l'intera frase rispetto alla chiave
        similarity_full_phrase = SequenceMatcher(None, input_phrase, key).ratio()
        
        if similarity_full_phrase >= threshold:
            matches.append((key, value))
            continue
        
        # Controlla ogni parola separatamente
        for word in words:
            if word in key:
                matches.append((key, value))
                break  # Evita duplicati aggiuntivi
            else:
                similarity = SequenceMatcher(None, word, key).ratio()
                if similarity >= threshold:
                    matches.append((key, value))
                    break  # Evita duplicati aggiuntivi

    # Rimuove duplicati e ordina per similarità se necessario
    matches = list(set(matches))
    matches.sort(key=lambda x: SequenceMatcher(None, input_phrase, x[0]).ratio(), reverse=True)
    
    return matches