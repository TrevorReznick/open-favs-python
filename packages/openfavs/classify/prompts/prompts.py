
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

def refactor_classify_agent(my_string, title, description, name, content):
    
    res_obj = crea_mappa_gerarchica(area_categories)    
    areas = ", ".join([f"{item['area']}" for item in area_categories])
    categories = ", ".join([f"{item['category']}" for item in area_categories])
    
    
    prompt = f"""
    
        **Task 1**:
        
        You should examine some website elements and give a classification respecting the tree of {res_obj};
        1. you will examinate first {title}, to undestand if it matchs with area list - {areas} - and categories list - {categories} - 
        2. you will examinate after {description}, to undestand if it matchs with area list - {areas} - and categories list - {categories} -
        3. as help for your tasks, we have a raw expalation text - {my_string} - with wich you will also understand if it matchs with area list - {areas} - and categories list - {categories} -
        4. well undestood the classification of the elements of points above, you will determitate exactly 5 tags in the followin way:
        
        1. select the most relevant main category as first tag;
        2. from the main associated categories, choose the most relevant category;
        3. from the categories associated sub category list, choose the most relevant sub-category as third tag;                
        4. you may select additional sub-categories the for the 4th and 5th tag
        5. To refine the classification, take a look to some text grabbed from the body site - {content}. This could provide a more precise context and better alignment of categorization.

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

        **Task 3**:
        Answear to this question, please: 'of given elements, the text - {my_string} is useful, or we can omit it?'; let me explain: the text come out from a first prompt, so if you don't need it, we optimize the flow with less requests.
        
        Good luck!       
    """
        
    return prompt
    
    
    
    
def create_reclassify_prompt(my_string, sub_cat_string, description, title):
    
    # @@ get new areas and categories @@ #
    # Passo 2: Estrapolare le aree
    
    areas = ", ".join([f"{item['area']}" for item in area_categories])
    
    categorie = ", ".join([f"{item['category']}" for item in area_categories])   
    
    sub_categorie = ", ".join([f"{sub['sub_category']}" for item in area_categories for sub in item['sub_categories']]) 
    
    mappa_gerarchica = crea_mappa_gerarchica(area_categories)
    
    mappa_gerarchica_string = json.dumps(mappa_gerarchica, ensure_ascii=False, indent=2)    
    
    prompt = f"""
        
        You should perform these 2 tasks:
        
        **Task 1**:
            Combining this text {description} and this text {my_string}, you should provide a classification based on the content 
            of this text {description}, you should compare it with this eleborated text {my_string}, providing a classification through 3 
            mandatory tags. You should follow these steps:
            
            1. From the main category list {areas}, select the most relevant main category as first tag;
            2. From the main associated categories {categorie}, choose the most relevant category as second tag considering informations provided by text {description};
            3. From the categories associated sub category list {sub_categorie}, choose the most relevant sub-category as third tag considering informations provided by text {description};                
            
            If fewer than 5 tags are appropriate, you may select additional sub-categories chosing from {sub_cat_string} to complete the 5 tags.
            
        **Task 2**: Argue the choices you have made, summarizing your reasoning as if it were 'your description' reworked for knowledge purposes. Start your summary with expressions such as 'The content was detected as...' or 'The resource provided belongs to the category...'. Make the best use of your knowledge.
        
        You should structure your answer by splitting the strict answer (Task 1) and the elaborated description (Task 2) using these rules:
        
        1. For Task 1, use a JSON object with this shape:
        
        {{
            'your_tag_1': selected_tag_1, 
            'your_tag_2': selected_tag_2, 
            'your_tag_3': selected_tag_3, 
            'your_tag_4': selected_tag_4,
            'your_tag_5': selected_tag_5
        }}

        2. For Task 2, provide the summary of your reasoning prefixed with 'my_string: '.

        Return the response as a string without spaces, prefixed with 'str_to_obj: ' followed by the JSON object string and the string of your notes of logic.
        3. For Task 3, simply answear to this question: can you read this object/dictionary: {mappa_gerarchica}?
        Good luck!
    """
    #print('prompt: ', prompt)
    return prompt

def create_classify_prompt(main_cat_str, description, suggestion, sub_cat_str):
        
    """
    Crea un prompt formattato per la classificazione basata su descrizione e lista di categorie.

    :param main_cat_str: Stringa delle categorie principali da cui scegliere.
    :param description: Descrizione da analizzare.
    :param suggestion: Suggerimento per la categoria principale.
    :param sub_cat_str: Stringa delle sottocategorie da cui scegliere i tag.
    :return: Una stringa di prompt formattata.
    """
    
    prompt = f"""
        You should be so skilled to identify the main_category one solely by from the choosing list: {main_cat_str} analyzing the description: {description} 
        and if there is suggestion {suggestion} give it as main_category; furthermore, you should find 5 tags exclusively from the list: {sub_cat_str} 
        and classify the site you are analyzing by providing 5 classify tags; the tags in the list should already be exhaustive for the classification 
        we intend to do, but only if you cannot find tags adaptable to the description, then you will suggest new tags, using the formula: suggested tags -> tags, 
        inserting them separately in the list of results of which you will find the formatting rules later.
        I please you to split the strict answer question, the classification, and notes of the logic you have used using the following rules: use a json object with 
        this shape: 
        {{
            'main_category': category, 
            '(your)tag_1': your_tag_1, 
            'your_tag_2': your_tag_2, 
            'your_tag_3': your_tag_3, 
            'your_tag_4': your_tag_4,
            'your_tag_5': your_tag_5,
            ***'suggested_tag_n': suggested_tag_n***
        }};
        the response will be a string without spaces, prefixed with str_to_obj: the json_object_string, a string of the notes of logic prefixed with 'my_string: ""'
        thanks a lot!
    """
    
    return prompt


#request_old = f"""
#You should be so skilled to identify the main_category one solely by from the choosing list: {main_cat_str} analizyng the description: {description};
#furthermore, you should find 5 tags exclusively from the list:  {sub_cat_str} and classify the site you are analizyng by providing 5 classify tags.
#There are 2 based data strings, main category: {main_cat_str} and sub category: {sub_cat_str}, a description {description}, a site content: {html_content} 
#and a suggestion {suggestion} for main category; can you give me 1 main category, consider suggestion if present and 5 sub category tags, 
#from provided strings within the description? if description has not suitable informations, you will consider the whole site content provided? 
#I please you to split the strict answer question, classification, parsed in markdown, and enventual notes of the logic you have used; 
#last part is optional. Thanks a lot!
#"""
"""
        You should perform these 2 tasks: Task 1 - Based on the content of this text {my_string} you should provide 1 main category and 5 tags to classify 
        the provided text; feel free to use tags you want, but there is a list of suggested main_cat {main_cat_str} and a list of {sub_cat_str} that should 
        be already be exhaustive for the classification  we intend to do; focusing on developement, when you will do the classification you will inspire to 
        the list {inspiration}; Task 2 - You shoud argue the choices you have made, trying to summarize your reasoning as if it were 'your description' reworked 
        for knowledge purposes: you should start your summary with expressions such as 'the content was detected...' or 'the content of the site is...' or 'the 
        resource provided belongs to the category...'; make the best use of your knowledge if is possible. I please you to split the strict answer question, 
        the classification - task-1, and the elaborated description (the notes of 
        the logic you have used reworked); please do it through these rules: 
        use a json object with this shape: 
        {{
            'main_category': category, 
            'tag_1': your_tag_1, 
            'tag_2': your_tag_2, 
            'tag_3': your_tag_3, 
            'tag_4': your_tag_4,
            'tag_5': your_tag_5,
            ***'suggested_tag_n': suggested_tag_n***
        }};        
        the response will be a string without spaces, prefixed with str_to_obj: the json_object_string, a string of the 
        notes of logic that you used prefixed with 'my_string: ""'
        good luck!
    """   
