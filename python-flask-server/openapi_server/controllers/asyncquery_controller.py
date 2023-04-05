import connexion
import six

from openapi_server.models.async_query_response import AsyncQueryResponse  # noqa: E501
from openapi_server import util


def asyncquery_post(request_body):  # noqa: E501
    """Initiate a query with a callback to receive the response

     # noqa: E501

    :param request_body: Query information to be submitted
    :type request_body: Dict[str, ]

    :rtype: AsyncQueryResponse
    """
    return 'do some magic!'
