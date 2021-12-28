import pprint
from duckduckgo_search import ddg

class Search:
    def __init__(self, keywords='', max_results=5, pdf=True):
        self.keywords = keywords
        self.max_results = max_results
        self.results = ddg(f'{self.keywords} filetype:pdf' if pdf else self.keywords, region='us-en', safesearch='Moderate', time=None, max_results=self.max_results)
    
    def print_results(self):
        pprint.pp(self.results, indent=4)
    
    def get_result(self, resid=0):
        return self.results[resid]