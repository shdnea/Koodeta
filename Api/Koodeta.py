import re

def slashInput(pattern, text):
    indexes = [match.start() for match in re.finditer(pattern, text)]
    return indexes