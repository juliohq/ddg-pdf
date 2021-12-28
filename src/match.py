import re

def match(search):
    matches = []
    for res in search.results:
        match = re.match(r'\S+\.pdf(?!\S)', res['href'])
        matches.append(res if match else None)
    return matches