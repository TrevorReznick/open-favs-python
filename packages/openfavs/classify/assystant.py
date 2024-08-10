class Config:
    MODEL = "gpt-35-turbo"
    START_PAGE = ""
    WELCOME = "Benenuti nell'assistente virtuale di Openfavs"
    ROLE = """
        You are an data entry analist of this site. You should have to classify a bookmark site
        after you grab the default information..
    """
    EMAIL = "enzonav@yahoo.it"
    THANKS = ""
    ERROR = ""
    OUT_OF_SERVICE = ""
    INAPPROPRIATE = ""

def main(args):
    print(args)