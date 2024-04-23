import connexion
import six
from typing import Dict
from typing import Tuple
from typing import Union

from openapi_server.models.meta_knowledge_graph import MetaKnowledgeGraph  # noqa: E501
from openapi_server import util

# geneticspro specific imports
from openapi_server.models.meta_node import MetaNode  # noqa: E501
from openapi_server.models.meta_edge import MetaEdge  # noqa: E501
from openapi_server.dcc.biolink_utils import create_predicate_triple_list, get_node_map



# def meta_knowledge_graph_get():  # noqa: E501
#     """Meta knowledge graph representation of this TRAPI web service.

#      # noqa: E501


#     :rtype: Union[MetaKnowledgeGraph, Tuple[MetaKnowledgeGraph, int], Tuple[MetaKnowledgeGraph, int, Dict[str, str]]
#     """
#     return 'do some magic!'



def meta_knowledge_graph_get():  # noqa: E501
    """Meta knowledge graph representation of this TRAPI web service.
     # noqa: E501
    :rtype: Union[MetaKnowledgeGraph, Tuple[MetaKnowledgeGraph, int], Tuple[MetaKnowledgeGraph, int, Dict[str, str]]
    """
    # return 'do some magic!'

    # initialize
    nodes = {}
    edges = []

    # build the nodes
    map_node = get_node_map()
    for key in map_node.keys():
        nodes[key] = MetaNode(id_prefixes=map_node.get(key), attributes=[])

    # build the edges
    list_edge = create_predicate_triple_list()
    for item in list_edge:
        edges.append(MetaEdge(subject=item[0], predicate=item[1], object=item[2], knowledge_types=[], attributes=[], qualifiers=[]))

    # build the knoelwdge map and return
    return MetaKnowledgeGraph(nodes=nodes, edges=edges)
