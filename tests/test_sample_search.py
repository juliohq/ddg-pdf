import unittest

from src.search import Search
from src.match import match

class TestSampleSearch(unittest.TestCase):
    def test_sample_search(self):
        search = Search('google', 5, pdf=False)
        # search.print_results()
        
        # test Search class
        self.assertEqual(search.keywords, 'google')
        self.assertEqual(search.max_results, 5)
        
        # test search results
        self.assertTrue(search.results)
        
        # test results' list length
        self.assertGreaterEqual(len(search.results), 5)
        
        # get specific result
        res = search.get_result()
        print(res)
        self.assertTrue(res)
        
        self.assertEqual(search.get_result(0), search.get_result())
    
    def test_sample_pdf_search(self):
        search = Search('python filetype:pdf', pdf=False)
        # search.print_results()
        
        # test search results
        self.assertTrue(search.results)
        
        # test whether it's a PDF file
        matches = match(search)
        self.assertTrue(any(matches))

if __name__ == "__main__":
    unittest.main()