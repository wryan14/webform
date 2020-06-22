# crossref API
from crossref.restful import Works
import requests
from lxml import etree
import pandas as pd  
import os

directory = os.path.dirname(__file__)
static_path = os.path.join(directory, 'static')


def crossref_lookup(doi_string, field):
    '''Uses crossref API to find record by DOI string'''
    w = Works()  # sets up crossref API object
    item = w.doi(doi_string)
    try:
        return item[field]
    except (KeyError, IndexError, TypeError):
        pass


def cdm_api_trans():
    '''Transforms CDM API FWP output into a dataframe for easier use.
    Works by using etree to run an XSLT script that converts XML to an
    HTML table. Pandas can then read the HTML table.'''
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


def cdm_pull(query_string):
    '''Function to pull from CONTENTdm, which is the repository used by the final product.
    This function will be used by the "Edit Publication" view in views.py to pull up existing records.
    :TODO: Consider various ways of pulling up records in a user-friendly way [Title? DOI? URL?]'''

    # please note that this will pull dummy XML data with the needed schema; there will be no API call until production

    # s = requests.Session()
    # res = s.get(query, verify=True)
    #root = etree.fromstring(res.content)

    # temporary code
    dummy_data = os.path.join(static_path, 'dummydata.xml')
    root = etree.parse(dummy_data)

    df = pd.read_html(str(cdm_api_trans()(root)))[0]  # read html table
    return df

