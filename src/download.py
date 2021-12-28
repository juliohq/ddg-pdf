import os
import urllib.request, urllib.error
from urllib.parse import urlparse

from src.match import match
from src.search import Search

DEST_PATH = os.path.join(os.getcwd(), 'output')

# hooks
create_folder_hook = []
skip_nonpdf_hook = []
http_error_hook = []

def download(search):
    results = search.results
    matches = match(search)
    
    if not os.path.isdir(DEST_PATH):
        for func in create_folder_hook:
            func(DEST_PATH)
        os.mkdir(DEST_PATH)
    
    for res in results:
        # skip if it's not a PDF file
        if not res in matches:
            for func in skip_nonpdf_hook:
                func(res)
            print("Skipping non-PDF file:", res['href'])
            continue
        
        try:
            # open result url
            url = res['href']
            http = urllib.request.urlopen(url)
            
            # get final url and set a file path for it
            path = os.path.join(DEST_PATH, os.path.basename(urlparse(http.geturl()).path))
            
            # retrieve file from final url
            furl = urllib.request.urlopen(http.geturl())
            print("Final url:", furl.geturl())
            txt = furl.read()
        except urllib.error.HTTPError as e:
            for func in http_error_hook:
                func(e)
            print("HTTP Error:", furl.geturl())
            continue
        
        # save to disk
        try:
            with open(path, 'wb') as f:
                f.write(txt)
        except IsADirectoryError:
            print("Path is a directory: couldn't download PDF from", furl.geturl())
            return

def download_search(keywords='', max_results=5):
    search = Search(keywords=keywords, max_results=max_results)
    download(search)