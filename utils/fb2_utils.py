import re

def strip_tags(rawtext):
    text = re.sub("<p>", "\n\t", rawtext)
    text = re.sub("<.+?>", "", rawtext)
    return text