import os
import urllib.request, urllib.error
from urllib.parse import urlparse

from src.match import match
from src.search import Search
from src.hash import get_hash, get_hash_raw

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
        url = res['href']
        
        # skip if it's not a PDF file
        if not res in matches:
            for func in skip_nonpdf_hook:
                func(res)
            print("Skipping non-PDF file:", url)
            continue
        
        try:
            # open result url
            http = urllib.request.urlopen(url)
            
            # get final url and set a file path for it
            path = os.path.join(DEST_PATH, os.path.basename(urlparse(http.geturl()).path))
            
            # retrieve file from final url
            fhttp = urllib.request.urlopen(http.geturl())
            furl = fhttp.geturl()
            print("url:", furl)
            txt = fhttp.read()
            if not txt[0:4] == b'%PDF':
                for func in skip_nonpdf_hook:
                    func(res)
                print("Skipping non-PDF file:", furl)
                continue
            # check if file already exists
            if os.path.isfile(path):
                dlhash = get_hash_raw(txt)
                fhash = get_hash(path)
                if dlhash == fhash:
                    print(f'Skipping already downloaded file\n{fhash}')
                    continue
                else:
                    print(f'Overwriting file with the same name: {path}')
        except urllib.error.HTTPError as e:
            for func in http_error_hook:
                func(e)
            print("HTTP Error:", furl)
            continue
        
        # save to disk
        with open(path, 'wb') as f:
            f.write(txt)

def download_search(keywords='', max_results=5):
    search = Search(keywords=keywords, max_results=max_results)
    download(search)