from difflib import SequenceMatcher 

def find_partial_matches(input_phrase, dictionary, threshold=0.8):
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