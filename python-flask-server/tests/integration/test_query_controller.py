# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from openapi_server.models.message import Message  # noqa: E501
from openapi_server.test import BaseTestCase


# files
file_gene_query = "tests/data/queryGenePayload.json"

class TestQueryController(BaseTestCase):
    """QueryController integration test stubs"""

    def test_query(self):
        """Test case for query

        Query reasoner via one of several inputs
        """

        # get the data
        with open(file_gene_query) as json_file:
            # read the map
            request_body = json.load(json_file)
        # request_body = None

        # call the service
        response = self.client.open(
            # '/query',
            '/genetics_provider/trapi/v1.2/query',
            method='POST',
            data=json.dumps(request_body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
