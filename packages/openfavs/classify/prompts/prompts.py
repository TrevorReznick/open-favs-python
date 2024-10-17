
import json
from load_json import area_categories, main_cat, sub_cat

from utils import get_complex_obj

# @@ get the cats json object @@ #

#main_cat_str = ", ".join([f"{item['cat_name']}" for item in main_cat])
#sub_cat_str = ", ".join([f"{item['cat_name']}" for item in sub_cat])

#id_category = [{"id": item["id"], "category": item["category"]} for item in area_categories]

areas = [f"{area['id']}:{area['area']}" for area in area_categories]

def new_summarize_prompt(name, title, description, content):
    prompt = f"""
        Analyze the following information with the provided fields (name, title, description, content) and 
        structure a detailed summary as follows:
        Key Points: 
            Break down the main points in each section, using a coded format (e.g., A1, A2, etc.).
            For name: Describe the platform or individual’s primary identity.
            Example: 
                A1: DEV Community - an online platform for developers. For title: Summarize the main title's significance.
            Example: 
                A2: Title signifies the community focus for coders. For description: List the key descriptive elements.
            Example: 
                A3: "We're a place where coders share, stay updated, and grow their careers." For content: Extract main 
                    points from the content using A4, A5, etc.
            Example: 
                A4: 
                    Emphasis on knowledge sharing.
                A5: 
                    Mentions of events like Hacktoberfest and career growth. 
        Underlying Argument: 
            Present the core argument by summarizing the implications and goals of the content. Use a coded format (e.g., B1, B2, etc.) 
                or clarity. 
            Example:
                B1: 
                    Encourages community engagement for skill development.
                B2: 
                    Advocates for staying updated with industry trends.
        Conclusion: 
            Offer a succinct conclusion on the overall purpose and intent behind the provided fields. Use C1, C2, etc., for each conclusive 
            statement.
            Example:
                C1: 
                    Emphasizes the role of community for coder development.
                C2: Concludes that engagement leads to professional growth.
            
        Here are the details:
            Name: [{name}]
            Title: [{title}]
            Description: [{description}]
            Content: [{content}]
    """
    return prompt

def new_summarize_prompt_1(name, title, description, content):
    prompt = f"""
        "Analyze the following text and provide a detailed summary using the following structure:
            Key Points: List the main information points using a coded format. Use alphanumeric codes (e.g., A1, A2, etc.) for each key point.
            Example:
                A1: Brief description of the community's purpose.
                A2: Explanation of user engagement features.
                Underlying Argument: Summarize the core argument the text is conveying, using a similar coded format (e.g., B1, B2, etc.).
            Example:
                B1: Promotes knowledge sharing among coders.
                B2: Aims to foster professional growth.
                Conclusion: Provide a concise conclusion about the overall intent and meaning of the text, using C1, C2, etc., for each point.
            Example:
                C1: Highlights the value of a collaborative platform.
                C2: Emphasizes the importance of community engagement for personal and professional development.
                Here is the text: [Insert your text here]"
    """

def create_summarize_prompt(name, title, description, content):

    prompt = f"""
        Can you summarize the informations given by name -{name} -, title -{title} -, description - {description} - and the text - {content} -
        Can you guess the underhood argument they speaks about?
        Thanks!
    """
    return prompt

#def create_reclassify_prompt(main_cat_str, sub_cat_str, inspiration, my_string, areas):

def last_classify_agent(summary, name):
    
    areas = ", ".join(set([f"{item['area']}" for item in area_categories]))
    
    #res_obj = get_complex_obj(area_categories)    
    #print('areas', areas)
    #categories = ", ".join([f"{item['category']}" for item in area_categories])
    print('is AI summary', summary)
      
    # Definizione stringa di esempio
    tag_1 = "Intelligenza Artificiale, Data Science e Big Data"
    tag_1_id = 4
    tag_2 = "Tecnologie e metodologie per l'analisi dei dati"
    tag_2_id = 11
    tag_3 = "Big Data Management"
    tag_3_id = 24
    tag_4 = "Gestione delle Infrastrutture IT"
    tag_4_id = 4
    tag_5 = "Server-Side Rendering (SSR)"
    tag_5_id = 44
    my_string = (
        "The site Example provides a comprehensive collection of headlines, "
        "snippets, and summaries across a wide array of topics, touching on weather, politics, "
        "crime, sports, economy, technology, social issues, education, opinions, and human interest stories. "
        "Given the diverse content..."
    )    
    stringa = (
        f'tag_1="{tag_1_id}:{tag_1}"&tag_2="{tag_2_id}:{tag_2}"&tag_3="{tag_3_id}:{tag_3}"&tag_4="{tag_4_id}:{tag_4}"&tag_5="{tag_5_id}:{tag_5}"&my_string="{my_string}"'
    )
    
    prompt = f"""
    
        **Task 1**:

        We provided a text for you; You should examine the text  - {summary} - and give, as if possible, a classification 
            respecting the tree of {area_categories} and a association between id:*field*; the association is mandatory, you cannot 
            output different results then the stringa - {stringa} - example format
        1. Select the most relevant area as the first tag. The service we are working prioritizes the matching of the 
            areas from the list - {areas} -, in format id:area.
            If the website being analyzed does not align with any of the topics in this list, return 'N/A' as described below.
            Consider we are working to add other categories, so the 'N/A' will help us to improve our work;
        2. from the main associated areas, choose the most relevant category from the dictionary - {area_categories} -; matching 
            the category you will associates the id how explained below;
        3. from the areas and associated category list, choose the most relevant sub-category as third tag;                
        4. you may select additional sub-categories the for the 4th and 5th tag, matching exactly the sub tree of already matched 
            categories and sub category from the dictionary - {area_categories}
        5. for the second tag, return the id of the matched category and the category name, using the : separator;
        6. for the 3th, 4th, 5th tag, return the id of the matched sub-category and the name, using the : separator; if you don't 
            find suitable items, return numeric:string values -1:N/A'
            
        Post scriptum: the association between id:*field* is mandatory, you cannot output different results

        **Task 2**: 
        
        Argue the choices you have made, summarizing your reasoning as if it were 'your description' reworked for knowledge purposes.         
        Start your summary using the name - {name} - capitalized, omitting phrases as 'the site #name# is...', 'the site #name# belongs 
        to...',  'the site #name# concern..' etc, starting with '#name# is'. Make the best use of your knowledge.        
        You should structure your answer by splitting the strict answer (Task 1) and the elaborated description (Task 2) using these rules:
        return a unique string, with key=values separated by &; 
        Here is an example:
                    
            {stringa}            
        
        Good luck!       
    """
        
    return prompt

