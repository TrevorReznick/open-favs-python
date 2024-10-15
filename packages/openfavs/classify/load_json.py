
import json
import os
print("Current working directory:", os.getcwd())

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Carica i dati dal file JSON
main_cat = load_json('json/main_cat.json')
sub_cat = load_json('json/sub_cat.json')
area_categories = load_json('json/areas_categories.json')


