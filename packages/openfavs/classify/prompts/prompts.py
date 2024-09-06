
import json
from load_json import area_categories, main_cat, sub_cat

from utils import get_complex_obj

# @@ get the cats json object @@ #

main_cat_str = ", ".join([f"{item['cat_name']}" for item in main_cat])
sub_cat_str = ", ".join([f"{item['cat_name']}" for item in sub_cat])

def create_summarize_prompt(name, title, description, content):

    prompt = f"""
        Can you summarize the informations given by name -{name} -, title -{title} -, description - {description} - and the text - {content} -
        Can you guess the underhood argument they speaks about?
        Thanks!
    """
    return prompt

#def create_reclassify_prompt(main_cat_str, sub_cat_str, inspiration, my_string, areas):

def last_classify_agent(summary, name):
    
    res_obj = get_complex_obj(area_categories)
    print('mappa gerarchica ', get_complex_obj(area_categories))
    areas = ", ".join([f"{item['area']}" for item in area_categories])
    categories = ", ".join([f"{item['category']}" for item in area_categories])
    
    # Definizione stringa di esempio
    tag_1 = "Intelligenza Artificiale, Data Science e Big Data"
    tag_2 = "Tecnologie e metodologie per l'analisi dei dati"
    tag_3 = "Big Data Management"
    tag_4 = "Gestione delle Infrastrutture IT"
    tag_5 = "Server-Side Rendering (SSR)"
    my_string = (
        "The site Example provides a comprehensive collection of headlines, "
        "snippets, and summaries across a wide array of topics, touching on weather, politics, "
        "crime, sports, economy, technology, social issues, education, opinions, and human interest stories. "
        "Given the diverse content..."
    )    
    stringa = (
        f'tag_1="{tag_1}"&tag_2="{tag_2}"&tag_3="{tag_3}"&tag_4="{tag_4}"&tag_5="{tag_5}"&my_string="{my_string}"'
    )
    
    prompt = f"""
    
        **Task 1**:

        We provided a text for you; You should examine the text {summary} and give, as if possible, a classification respecting the tree of {res_obj};
                
        1. select the most relevant area as first tag;
        2. from the main associated areas, choose the most relevant category;
        3. from the areas and associated sub category list, choose the most relevant sub-category as third tag;                
        4. you may select additional sub-categories the for the 4th and 5th tag, matching exactly the sub tree of already matched categories and sub category from the dictionary - {res_obj}
        5. for the 3th, 4th, 5th tag, return the id of the matched sub-category and the name, using the : separator; if you don't find suitable items, return 'null:N/A'

        **Task 2**: 
        
        Argue the choices you have made, summarizing your reasoning as if it were 'your description' reworked for knowledge purposes.         
        Start your summary using the name - {name} - capitalized (i.e. the site #name# is... the site #name# belongs to... the site #name# concern.. etc)
        Make the best use of your knowledge.        
        You should structure your answer by splitting the strict answer (Task 1) and the elaborated description (Task 2) using these rules:
        return a unique string, with key=values separated by &; 
        Here is an example:
            
            {stringa}         
        
        Good luck!       
    """
        
    return prompt

