import unittest  
import os  
import logging  
import sys  
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.join(testdir, srcdir))
from app.utility import CRef, cdm_pull  

# create directory for logging and testing
directory = os.path.dirname(os.path.abspath(__file__))
logs_path = os.path.join(directory, 'logs')
logs_file = os.path.join(logs_path, 'logs.txt')

if not os.path.exists(logs_path):
    os.makedirs(logs_path)  

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, filename=logs_file, filemode='a')

class UtilityTest(unittest.TestCase):

    def test_cref_doi(self):
        '''Make sure the crossref lookup utility function is operating correctly'''
        cr = CRef('http://doi.org/10.17016/FEDS.2020.013')
        self.assertTrue(cr.doi=='10.17016/FEDS.2020.013')
    
    def test_cref_author_list(self):
        '''Ensure Cref returns correct author list'''
        cr = CRef('10.17016/FEDS.2020.049')
        self.assertTrue(cr.author_list == ['Bekaert, Geert', 'Engstrom, Eric', 'Ermolov, Andrey'])
        
    def test_cref_journal_title(self):
        '''See if container-title returns journal on known DOI'''
        cr = CRef('10.17016/FEDS.2020.049')
        self.assertTrue(cr.journal_name=='Finance and Economics Discussion Series')

    def test_remaining_cref_fields(self):
        '''Quick check to make sure other fields are working; please not it is possible that if CrossRef's
        Metadata changes, this might impact the validity of this test. '''
        cr = CRef('10.31274/etd-180810-5803')
        self.assertTrue(cr.journal_name=='')
        self.assertTrue(cr.title=='Faculty perceptions regarding the infusion of global perspectives into the College of Agriculture and Life Sciences curriculum: A comparative study')
        self.assertTrue(cr.publisher=='Iowa State University')
        self.assertTrue(cr.author_list==['Magtoto, Ronaldo Lising'])
        self.assertTrue(cr.year==2020)


    def test_cdm_pull_columns(self):
        '''Test to make sure columns correctly translate'''
        
        expected_columns = ['Creator', 'Title', 'Date', 'Date-Created', 'JEL Codes', 'Subject',
                            'Publisher', 'Published in', 'Cite as', 'Citation markup',
                            'Earlier versions', 'Later versions', 'Volume', 'Issue', 'Identifier',
                            'm1', 'Division affiliation', 'Quarter', 'Public address',
                            'Link to article', 'DOI_Number']

        df = cdm_pull('argument not needed in test environment')
        self.assertTrue(df.columns.tolist()==expected_columns)

    def test_cdm_pull_data(self):
        '''Check to make sure the correctly carries over form XML to dataframe'''
        df = cdm_pull('argument not needed in test environment')

        self.assertTrue(df['Creator'].tolist()[0]=='McGucken, Correna; Farington, Boote; St., Courtnay')
        self.assertTrue(df['Title'].tolist()[0]=='She Gods of Shark Reef')
        self.assertTrue(df.shape[0]==1000)




if __name__=="__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
        
