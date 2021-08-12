
# imports
import pytest 
from openapi_server.dcc.utils import get_curie_synonyms

# def get_curie_synonyms(curie_input, prefix_list=None, type_name='', log=False):
def test_get_curie_synonyms():
    ''' test the curie synonym resolution '''

    # test curie that matches already
    curie = 'EFO:0000289'
    name, result = get_curie_synonyms(curie, ['EFO', 'MONDO'], log=False)
    assert len(result) == 2
    assert curie in result

    # test no curie
    curie = None
    name, result = get_curie_synonyms(curie, ['EFO', 'MONDO'])
    assert len(result) == 1
    assert result[0] == curie
    assert result[0] is None

    # test no curie
    curie = "NCIT:C122516"
    name, result = get_curie_synonyms(curie, ['EFO', 'MONDO'])
    assert len(result) == 0
