# crossref API
from crossref.restful import Works


def crossref_lookup(doi_string, field):
    '''Uses crossref API to find record by DOI string'''
    w = Works()  # sets up crossref API object
    item = w.doi(doi_string)
    try:
        return item[field]
    except (KeyError, IndexError, TypeError):
        pass
