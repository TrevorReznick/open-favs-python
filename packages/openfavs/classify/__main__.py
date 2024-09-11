#--web true
#--kind python:default

import json

import assistant
import url_control


def main(args):

    #print('hello from main')    
    #return json.dumps(response)

    url = args.get('url')
    
    if(url):
        
        control_url = url_control.WebControl(url)
        
        test_site = control_url.validate_site()
        
        print('hello', test_site)
        
        #print(control_url.get_url_info())
        if(control_url.validate_url()):
            #print('url corretto!')
            #print('debug main url', url)
            return assistant.main(args)
    else:
        print('errore url')
        return None
        
    """
    return { 
        "body": doc_assistant.main(args)
    }
    """
args = {}
main(args)