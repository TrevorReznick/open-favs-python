#--web true
#--kind python:default

import json

import assistant
import web_control


def main(args):

    #print('hello from main')    
    #return json.dumps(response)

    url = args.get('url')
    
    if(url):
        url_control = web_control.WebControl(url)
        #print(url_control.get_url_info())
        if(url_control.validate_url()):
            print('url corretto!')
            #print('main url arg', url)
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