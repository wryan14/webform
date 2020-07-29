# utility.py
# file contains python functions that assist with gathering data for main application

from crossref.restful import Works
import requests
from lxml import etree
import pandas as pd
import os

directory = os.path.dirname(__file__)
static_path = os.path.join(directory, 'static')


class CRef():
    """Leverages the crossref.restful API to gather metadata requried to submit a new publication
    to the web form. The crossref schema can be found at https://data.crossref.org/schemas/crossref_query_input2.0.xsd.

    This class parses in a way that satisfies the needs of the Economist Webform project. If you need different metadata, 
    modify this class to target different fields. 

    :param doi: Digital object identifier (doi); URL like string associated with a publication registered with CrossRef
    :type doi: str

    Attributes:
        :doi (str): same as param
        :res (obj): response to the crossref.restful API call
        :title (str): title of the document returned in API call
        :publisher(str): name of publisher of document from API call
        :journal_name (str): publication which houses document returned in API call
        :year (str): year returned document was published
    """

    def __init__(self, doi):
        # make sure prefix is removed
        self.doi = doi.strip(
            'https://doi.org/').strip('http://doi.org/').strip()

        w = Works()
        self.res = w.doi(self.doi)

        self.title = self.res['title'][0].replace(
            '\t', ' ').replace('\n', ' ').replace('  ', ' ')
        self.title = ' '.join([x for x in self.title.split() if x != ' '])

        self.publisher = self.tryfield('publisher')
        try:
            self.journal_name = self.tryfield('container-title')[0]
        except IndexError:
            self.journal_name = ''

        self.author_find()  # get authors

        try:
            self.year = self.res['indexed']['date-parts'][0][0]
        except (KeyError, IndexError):
            self.year = ''

    def author_find(self):
        """Method to find and parse a list of authors returned in crossref.restful API
        response. 

        Attributes:
            :author_list (list): list of authors ['lastname, firstname',] from API response
        """
        self.author_list = []
        for auth in self.res['author']:
            try:
                self.author_list.append('{}, {}'.format(
                    auth['family'], auth['given']))
            except KeyError:
                pass

    def tryfield(self, field):
        try:
            return self.res[field]
        except KeyError:
            return ''


def cdm_api_trans():
    """Pythonic approach to running XSLT transformation.  The transformation takes CONTENTdm's
    API response and converts the XML into HTML tables, which, in turn, can be converted to a pandas
    dataframe.
    """
    xsl_root = etree.XML('''\
    <xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <table border="1">
            <tr>
                <th>Creator</th>
                <th>Title</th>
                <th>Date</th>
               <th>Date-Created</th>
                <th>JEL Codes</th>\
                <th>Subject</th>
                <th>Publisher</th>
                <th>Published in</th>
                <th>Cite as</th>
                <th>Citation markup</th>
                <th>Earlier versions</th>
                <th>Later versions</th>
                <th>Volume</th>
                <th>Issue</th>
                <th>Identifier</th>
                <th>m1</th>
                <th>Division affiliation</th>
                <th>Quarter</th>
                <th>Public address</th>
                <th>Link to article</th>
                <th>DOI_Number</th>
            </tr>
            <xsl:apply-templates />
        </table>
    </xsl:template>
    <xsl:template match="records">
        <xsl:for-each select="record">
            <tr>
                <td>
                    <xsl:value-of select="creata"/>
                </td>
                <td>
                    <xsl:value-of select="title" />
                </td>
                <td>
                    <xsl:value-of select="date" />
                </td>
                <td>
                    <xsl:value-of select="dmcreated" />
                </td>
                <td>
                    <xsl:value-of select="jel" />
                </td>
                <td>
                    <xsl:value-of select="subjec" />
                </td>
                <td>
                    <xsl:value-of select="publis" />
                </td>
                <td>
                    <xsl:value-of select="relatig"/>
                </td>
                <td>
                    <xsl:value-of select="identia"/>
                </td>
                <td>
                    <xsl:value-of select="citata" />
                </td>
                <td>
                    <xsl:value-of select="relatia" />
                </td>
                <td>
                    <xsl:value-of select="relatib" />
                </td>
                <td>
                    <xsl:value-of select="volume" />
                </td>
                <td>
                    <xsl:value-of select="issue" />
                </td>
                <td>
                    <xsl:value-of select="identi" />
                </td>
                <td>
                    <xsl:value-of select="m1" />
                </td>
                <td>
                    <xsl:value-of select="board" />
                </td>
                <td>
                    <xsl:value-of select="quarte" />
                </td>
                <td>
                    <xsl:value-of select="public" />
                </td>
                <td>
                    <xsl:value-of select="link" />
                </td>
                <td>
                    <xsl:value-of select="doi" />
                </td>
            </tr>
        </xsl:for-each>
    </xsl:template>
    </xsl:stylesheet>
    ''')

    return etree.XSLT(xsl_root)


def cdm_pull(query_string=None):
    """Calls CONTENTdm's API and runs the cdm_api_trans XSLT transformation against te results.  
    The function then converts the HTML tables from cdm_api_trans to a pandas dataframe, and
    returns the output.

    :param query_string: string that will return CDM API response with desired parameters
    :type query_string: str

    *Note* During the prototype stage of this project, this function will read in dummy data that replicates
    the CDM API response, instead of calling a live API.  Make sure dummydata.xml is located in the static directory.\
    """

    # please note that this will pull dummy XML data with the needed schema; there will be no API call until production

    # s = requests.Session()
    # res = s.get(query, verify=True)
    #root = etree.fromstring(res.content)

    # temporary code
    dummy_data = os.path.join(static_path, 'dummydata.xml')
    root = etree.parse(dummy_data)

    df = pd.read_html(str(cdm_api_trans()(root)))[0]  # read html table
    return df