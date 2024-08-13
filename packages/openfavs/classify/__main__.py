#--web true
#--kind python:default

import json

import assistant


def main(args):
    print('hello from main')    
    #return json.dumps(response)
    return assistant.main(args)
    """
    return { 
        "body": doc_assistant.main(args)
    }
    """
args = {}
main(args)