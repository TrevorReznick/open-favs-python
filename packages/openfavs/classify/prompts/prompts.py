
import json
from load_json import area_categories
from difflib import SequenceMatcher

def crea_mappa_gerarchica(data):
    mappa_gerarchica = {}

    for item in data:
        area = item['area']
        categoria = item['category']
        sotto_categorie = [sub['sub_category'] for sub in item['sub_categories']]

        if area not in mappa_gerarchica:
            mappa_gerarchica[area] = {}

        if categoria not in mappa_gerarchica[area]:
            mappa_gerarchica[area][categoria] = []

        mappa_gerarchica[area][categoria].extend(sotto_categorie)

    return mappa_gerarchica

def create_summarize_prompt(name, title, description, content):

    prompt = f"""
        Can you summarize the informations given by name -{name} -, title -{title} -, description - {description} - and the text - {content} -
        Can you guess the underhood argument they speaks about?
        Thanks!
    """
    return prompt

#def create_reclassify_prompt(main_cat_str, sub_cat_str, inspiration, my_string, areas):

def last_classify_agent(summary, name):
    
    res_obj = crea_mappa_gerarchica(area_categories)    
    areas = ", ".join([f"{item['area']}" for item in area_categories])
    categories = ", ".join([f"{item['category']}" for item in area_categories])
    
    
    prompt = f"""
    
        **Task 1**:

        We provided a text for you; You should examine the text {summary} and give, as if possible, a classification respecting the tree of {res_obj};
                
        1. select the most relevant main category as first tag;
        2. from the main associated categories, choose the most relevant category;
        3. from the categories and associated sub category list, choose the most relevant sub-category as third tag;                
        4. you may select additional sub-categories the for the 4th and 5th tag, tring to respect the {res_obj}

        **Task 2**: 
        
        Argue the choices you have made, summarizing your reasoning as if it were 'your description' reworked for knowledge purposes.         
        Start your summary using the name - {name} - capitalized (i.e. the site #name# is... the site #name# belongs to... the site #name# concern.. etc)
        Make the best use of your knowledge.        
        You should structure your answer by splitting the strict answer (Task 1) and the elaborated description (Task 2) using these rules:
        
        1. use a JSON object with this shape:
        
        {{
            'tag_1': selected_tag_1, 
            'tag_2': selected_tag_2, 
            'tag_3': selected_tag_3, 
            'tag_4': selected_tag_4,
            'tag_5': selected_tag_5
        }}

        2. For Task 2, provide a string, in conversional mode, with the summary of your reasoning prefixed with 'my_string: ' - your notes of logic -.
        
        3. so this should have to be the final obj:
        
        {{
            'tag_1': selected_tag_1, 
            'tag_2': selected_tag_2, 
            'tag_3': selected_tag_3, 
            'tag_4': selected_tag_4,
            'tag_5': selected_tag_5,
            'my_string': notes of logic
        }}
        
        Good luck!       
    """
        
    return prompt

