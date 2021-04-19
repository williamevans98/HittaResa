import wikipedia

wikipedia.set_lang("fr")

def get_wiki(search):
    wikipedia.summary(search, sentences=1)

    return wiki_search

test = "Hej"
get_wiki(test)

