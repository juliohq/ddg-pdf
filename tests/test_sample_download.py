import unittest

from src import download as dl

class TestSampleDownload(unittest.TestCase):
    def test_sample_download(self):
        dl.download_search('python')
        
        self.assertTrue(True)

if __name__ == "__main__":
    unittest.main()