import unittest  
import os  
import logging  
import sys  
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.join(testdir, srcdir))
from app.utility import crossref_lookup, cdm_pull  

directory = os.path.dirname(os.path.abspath(__file__))
logs_path = os.path.join(directory, 'logs')
logs_file = os.path.join(logs_path, 'logs.txt')

if not os.path.exists(logs_path):
    os.makedirs(logs_path)  

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=logs_file, filemode='a')

class UtilityTest(unittest.TestCase):

    def test_crossref_lookup(self):
        '''Make sure the crossref lookup utility function is operating correctly'''
        name = crossref_lookup('10.17016/FEDS.2020.013', 'title')[0]
        self.assertTrue(name=='Inflation at Risk')


if __name__=="__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
        
