
#import packages.openfavs.classify.get_site_info_old as get_site_info_old
from openai import AzureOpenAI, BadRequestError
import get_site_info, packages.openfavs.classify.url_control as url_control, get_info
from load_json import main_cat, sub_cat, area_categories
from utils import find_partial_matches, find_partial_matches_new, split_sentence, create_phrases_dict, extract_json, extract_my_string
from prompts.prompts import create_summarize_prompt, last_classify_agent

class Config:
    #MODEL = "gpt-4"ss  
    GPT_4 = "gpt-4"
    GPT_3 = "gpt-35-turbo"
    WELCOME = "Benenuti nell'assistente virtuale di Openfavs"
    #ROLE = "You are the Openfavs virtual assistant. The first answear to first input have to be: 'hello, i'm an Openfavs assistant. How can help you? "
    ROLE = "You are the Openfavs virtual assistant, your role is web site analyst, classifyng the input data"   
    SUPERVISOR_ROLE = "You are a supervisor of a data entry operator who has classified some resources. Your task is to is to provide answers in the third person, in a professional and friendly manner"
    GEMERIC_ROLE = "You are a generic GPT-4 assistant, provide kindly answers to user's questions"
    ERROR = "There was an error processing your request"
    OUT_OF_SERVICE = "We apogize, but the assistant is not available. Coming soon"
    INAPPROPRIATE = "Temo che la tua richiesta possa essere fraintesa. Puoi riformularla in maniera più appropriata?"
    SUGGESTIONS = {
        "cloud-native": "serverless",
        "portfolio": "inspiration",
        "projects": "inspiration",
        "full stack developer": "developement",
        "amministratore di sisteme": "system engineer"
    }
    RESERVED_WORDS = {
        "Code",
        "Development",
        "Deployment",
        "Hosting",
        "Versioning",
        "Continuous Integration",
        "Continuous Deployment",
        "Server",
        "Cloud",
        "Microservices",
        "Containerization",
        "Kubernetes",
        "Docker",
        "Pipeline",
        "Git",
        "GitHub",
        "GitLab",
        "Bitbucket",
        "Automation",
        "Jenkins",
        "CI/CD",
        "DevOps",
        "Infrastructure",
        "API",
        "RESTful",
        "GraphQL",
        "Load Balancer",
        "Replica",
        "Backup",
        "Scalability",
        "Performance",
        "Load Testing",
        "Staging",
        "Rollback",
        "Monitoring",
        "Log Management",
        "Ansible",
        "Terraform",
        "CloudFormation",
        "Infrastructure as Code",
        "Virtualization",
        "Security",
        "HTTPS",
        "SSL/TLS",
        "Firewall",
        "DNS",
        "CDN",
        "Serverless",
        "Edge Computing",
        "Scripting",
        "Container",
        "Orchestration",
        "Cluster",
        "Provisioning",
        "Scaling",
        "High Availability",
        "Fault Tolerance",
        "Blue-Green Deployment",
        "Canary Release",
        "Environment",
        "Artifact",
        "Build",
        "Test Automation",
        "Unit Testing",
        "Integration Testing",
        "Acceptance Testing",
        "Load Balancing",
        "Zero Downtime",
        "API Gateway",
        "Service Mesh",
        "IAM",
        "Secrets Management",
        "Configuration Management",
        "Infrastructure Monitoring",
        "Incident Response",
        "Alerting",
        "Observability",
        "Tracing",
        "Logging",
        "Metrics",
        "Stateful",
        "Stateless",
        "Hybrid Cloud",
        "Multi-Cloud",
        "Private Cloud",
        "Public Cloud",
        "Elasticity",
        "Networking",
        "VPC",
        "Subnet",
        "Firewall Rules",
        "Ingress",
        "Egress",
        "Load Testing",
        "Penetration Testing",
        "Static Code Analysis",
        "Dynamic Code Analysis",
        "Code Review",
        "Pull Request",
        "Merge",
        "Branch",
        "Feature Flags",
        "Rollout",
        "Rollback",
        "Secret Key",
        "Environment Variables"
    }
    
    


import re, json, os
import requests
from openai import AzureOpenAI, BadRequestError
from bs4 import BeautifulSoup
#import traceback, random
#from html_sanitizer import Sanitizer
#from urllib.parse import urlparse
#from difflib import SequenceMatcher

class ChatBot:

    def __init__(self, args):

        #print('init class chatbot')
        OPENAI_API_KEY = '89773db3-7863-460c-ad3c-6abd0db43f1c'
        OPENAI_API_HOST = 'https://openai.nuvolaris.io'      
        self.key = OPENAI_API_KEY
        self.host = OPENAI_API_HOST
        self.ai =  AzureOpenAI(
            api_version="2023-12-01-preview", 
            api_key=self.key, 
            azure_endpoint=self.host
        )

    def asks_ai(self, input, role):

        print('asking chatbot')
        #print('input', input)
        #print('role', role)

        req = [ 
            {"role": "system", "content": role}, 
            {"role": "user", "content": input}
        ]

        try:
            comp = self.ai.chat.completions.create(model=Config.GPT_4, messages=req)
            if len(comp.choices) > 0:
                content = comp.choices[0].message.content
                #print('debug chatbot')
                return content
            
        except BadRequestError as e:            
            return Config.INAPPROPRIATE
        
        except Exception as e:
            return Config.OUT_OF_SERVICE
        return None
        
        
class Website:

    def __init__(self, args):

        self.response = ""
        self.site_info = {}
        self.url = args.get("url")  
        #print('debug assistant', args)
        #self.sanitizer = Sanitizer()  
        #print('init class website')    
    

    def get_request(self, args):
        
        self.url = args.get("url")        
        extractor = get_site_info.MetaDataExtractor(args.get("url"))
        json_metadata = extractor.to_json()
        metadata_obj = json.loads(json_metadata)            
        return metadata_obj

    def get_request_new(self, args):
        self.url = args.get("url") 
        extractor = get_info.MetaDataExtractorNew(args.get("url"))
        print(extractor.extract_metadata())

AI = None
Web = None

def main(args):

    global AI, Web

    #print('into main')
    
    if AI is None: AI = ChatBot(args)    
    if Web is None: Web = Website(args)
    
    url = args.get("url")
    #print('init MetaDataExtractor class')
    extractor = get_site_info.MetaDataExtractor(url)    
    
    description = extractor.get_description()
    html_content = extractor.get_html_content()

    #
    if(description):
        #print('description exists :', description)
        a = 1
    else: 
        print('description not exists!')

   
    
    # @@ prod flow @@ #

        # qui viene seguito controllo se la pagina è accessibile o meno

    if(html_content):
        print('html content found!')

    else:
        url_utils = url_control.WebControl(url)
        url_logs = url_utils.get_url_info()
        print('html content not found; ', url_logs)
        print('debug html content found: ', url_utils.get_html_content())
        print('debug soup results: ', extractor.get_html_content())
        
    #print(html_content)

    returned_obj = Web.get_request(args)    
    
    #json_object = extract_json(classify, 'str_to_obj')
    #my_string = extract_my_string(classify, 'my_string')
    #result = {**json_object, **my_string} # Combina i risultati    
       
    reserved_words = ", ".join(Config.RESERVED_WORDS)
    title = extractor.get_title()
    name = returned_obj.get('name')   

    my_prompt = create_summarize_prompt(name, title, description, html_content)

    summarize = AI.asks_ai(my_prompt, Config.ROLE)
    #print(summarize)

    last_refactored_prompt = last_classify_agent(summarize, name)
    last_ai_request = AI.asks_ai(last_refactored_prompt, Config.ROLE)
    print('new_response: ', last_ai_request)
    Web.get_request_new(args)
    

    return {
        "body": returned_obj
    }
     
