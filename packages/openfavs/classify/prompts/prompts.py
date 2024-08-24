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
