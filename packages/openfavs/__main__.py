#--web true
#--kind python:default

#import doc_assistant

def main(args):
    print('hello from main')
    name = args.get("name", "world")
    greeting = "Hello " + name + "!"
    return {"body": greeting}
    """
    return { 
        "body": doc_assistant.main(args)
    }
    """
args = {}
main(args)