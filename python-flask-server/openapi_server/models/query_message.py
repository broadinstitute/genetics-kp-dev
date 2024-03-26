# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.auxiliary_graph import AuxiliaryGraph
from openapi_server.models.message import Message
from openapi_server.models.message_knowledge_graph import MessageKnowledgeGraph
from openapi_server.models.message_query_graph import MessageQueryGraph
from openapi_server.models.result import Result
from openapi_server import util

from openapi_server.models.auxiliary_graph import AuxiliaryGraph  # noqa: E501
from openapi_server.models.message import Message  # noqa: E501
from openapi_server.models.message_knowledge_graph import MessageKnowledgeGraph  # noqa: E501
from openapi_server.models.message_query_graph import MessageQueryGraph  # noqa: E501
from openapi_server.models.result import Result  # noqa: E501

class QueryMessage(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, results=None, query_graph=None, knowledge_graph=None, auxiliary_graphs=None):  # noqa: E501
        """QueryMessage - a model defined in OpenAPI

        :param results: The results of this QueryMessage.  # noqa: E501
        :type results: List[Result]
        :param query_graph: The query_graph of this QueryMessage.  # noqa: E501
        :type query_graph: MessageQueryGraph
        :param knowledge_graph: The knowledge_graph of this QueryMessage.  # noqa: E501
        :type knowledge_graph: MessageKnowledgeGraph
        :param auxiliary_graphs: The auxiliary_graphs of this QueryMessage.  # noqa: E501
        :type auxiliary_graphs: Dict[str, AuxiliaryGraph]
        """
        self.openapi_types = {
            'results': List[Result],
            'query_graph': MessageQueryGraph,
            'knowledge_graph': MessageKnowledgeGraph,
            'auxiliary_graphs': Dict[str, AuxiliaryGraph]
        }

        self.attribute_map = {
            'results': 'results',
            'query_graph': 'query_graph',
            'knowledge_graph': 'knowledge_graph',
            'auxiliary_graphs': 'auxiliary_graphs'
        }

        self._results = results
        self._query_graph = query_graph
        self._knowledge_graph = knowledge_graph
        self._auxiliary_graphs = auxiliary_graphs

    @classmethod
    def from_dict(cls, dikt) -> 'QueryMessage':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Query_message of this QueryMessage.  # noqa: E501
        :rtype: QueryMessage
        """
        return util.deserialize_model(dikt, cls)

    @property
    def results(self):
        """Gets the results of this QueryMessage.

        List of all returned Result objects for the query posed. The list SHOULD NOT be assumed to be ordered. The 'score' property, if present, MAY be used to infer result rankings. If Results are not expected (such as for a query Message), this property SHOULD be null or absent. If Results are expected (such as for a response Message) and no Results are available, this property SHOULD be an array with 0 Results in it.  # noqa: E501

        :return: The results of this QueryMessage.
        :rtype: List[Result]
        """
        return self._results

    @results.setter
    def results(self, results):
        """Sets the results of this QueryMessage.

        List of all returned Result objects for the query posed. The list SHOULD NOT be assumed to be ordered. The 'score' property, if present, MAY be used to infer result rankings. If Results are not expected (such as for a query Message), this property SHOULD be null or absent. If Results are expected (such as for a response Message) and no Results are available, this property SHOULD be an array with 0 Results in it.  # noqa: E501

        :param results: The results of this QueryMessage.
        :type results: List[Result]
        """
        if results is not None and len(results) < 0:
            raise ValueError("Invalid value for `results`, number of items must be greater than or equal to `0`")  # noqa: E501

        self._results = results

    @property
    def query_graph(self):
        """Gets the query_graph of this QueryMessage.


        :return: The query_graph of this QueryMessage.
        :rtype: MessageQueryGraph
        """
        return self._query_graph

    @query_graph.setter
    def query_graph(self, query_graph):
        """Sets the query_graph of this QueryMessage.


        :param query_graph: The query_graph of this QueryMessage.
        :type query_graph: MessageQueryGraph
        """

        self._query_graph = query_graph

    @property
    def knowledge_graph(self):
        """Gets the knowledge_graph of this QueryMessage.


        :return: The knowledge_graph of this QueryMessage.
        :rtype: MessageKnowledgeGraph
        """
        return self._knowledge_graph

    @knowledge_graph.setter
    def knowledge_graph(self, knowledge_graph):
        """Sets the knowledge_graph of this QueryMessage.


        :param knowledge_graph: The knowledge_graph of this QueryMessage.
        :type knowledge_graph: MessageKnowledgeGraph
        """

        self._knowledge_graph = knowledge_graph

    @property
    def auxiliary_graphs(self):
        """Gets the auxiliary_graphs of this QueryMessage.

        Dictionary of AuxiliaryGraph instances that are used by Knowledge Graph Edges and Result Analyses. These are referenced elsewhere by the dictionary key.  # noqa: E501

        :return: The auxiliary_graphs of this QueryMessage.
        :rtype: Dict[str, AuxiliaryGraph]
        """
        return self._auxiliary_graphs

    @auxiliary_graphs.setter
    def auxiliary_graphs(self, auxiliary_graphs):
        """Sets the auxiliary_graphs of this QueryMessage.

        Dictionary of AuxiliaryGraph instances that are used by Knowledge Graph Edges and Result Analyses. These are referenced elsewhere by the dictionary key.  # noqa: E501

        :param auxiliary_graphs: The auxiliary_graphs of this QueryMessage.
        :type auxiliary_graphs: Dict[str, AuxiliaryGraph]
        """

        self._auxiliary_graphs = auxiliary_graphs