#--web true
#--kind python:default

import json

#import doc_assistant


def main(args):
    print('hello from main')
    name = args.get("name", "world")
    greeting = "Hello " + name + "!"
    # return {"body": greeting}
    response = {"body": greeting}
    # Serializza il dizionario in una stringa JSON
    return json.dumps(response)
    """
    return { 
        "body": doc_assistant.main(args)
    }
    """
args = {}
main(args)