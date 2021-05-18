
# imports
import pytest 
from openapi_server.dcc.biolink_utils import make_into_array

def test_make_into_array():
    ''' test the make into array method '''

    simple_string = "test"
    result = make_into_array(simple_string)
    assert type(result) == type([])


