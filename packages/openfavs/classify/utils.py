import re
from difflib import SequenceMatcher 

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