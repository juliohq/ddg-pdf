import os
import http
import urllib.request, urllib.error
from urllib.parse import urlparse

from src.match import match
from src.search import Search
from src.hash import get_hash, get_hash_raw

DEST_PATH = os.path.join(os.getcwd(), 'output')

color_output = True
global_timeout = 10

# hooks
create_folder_hook = []
skip_nonpdf_hook = []
http_error_hook = []
url_error_hook = []

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
            out = f"\u001b[33mSkipping non-PDF file: {url}\u001b[37m" if color_output else f"Skipping non-PDF file: {url}"
            print(out)
            continue
        
        try:
            # open result url
            http = urllib.request.urlopen(url, timeout=global_timeout/2)
            
            # get final url and set a file path for it
            path = os.path.join(DEST_PATH, os.path.basename(urlparse(http.geturl()).path))
            
            # retrieve file from final url
            fhttp = urllib.request.urlopen(http.geturl(), timeout=global_timeout/2)
            furl = fhttp.geturl()
            print("url:", furl)
            txt = fhttp.read()
            if not txt[0:4] == b'%PDF':
                for func in skip_nonpdf_hook:
                    func(res)
                out = f"\u001b[33mSkipping non-PDF file: {furl}\u001b[37m" if color_output else f"Skipping non-PDF file: {furl}"
                print(out)
                continue
            # check if file already exists
            if os.path.isfile(path):
                dlhash = get_hash_raw(txt)
                fhash = get_hash(path)
                if dlhash == fhash:
                    out = f"\u001b[32mSkipping already downloaded file\n{fhash}\u001b[37m" if color_output else f"Skipping already downloaded file\n{fhash}"
                    print(out)
                    continue
                else:
                    print(f'Overwriting file with the same name: {path}')
        except urllib.error.HTTPError as e:
            for func in http_error_hook:
                func(e)
            out = f"\033[0;31mHTTP Error: {furl} \u001b[37m" if color_output else f"HTTP Error: {furl}"
            print(out)
            continue
        except urllib.error.URLError as e:
            for func in url_error_hook:
                func(e)
            out = f"\033[0;31mURL Error: {furl} \u001b[37m" if color_output else f"URL Error: {furl}"
            print(out)
            continue
        except http.client.IncompleteRead:
            out = f"\033[0;31mTimeout Error: {furl} \u001b[37m" if color_output else f"Timeout Error: {furl}"
            print(out)
            continue
        
        # save to disk
        with open(path, 'wb') as f:
            f.write(txt)

def download_search(keywords='', max_results=5):
    search = Search(keywords=keywords, max_results=max_results)
    download(search)