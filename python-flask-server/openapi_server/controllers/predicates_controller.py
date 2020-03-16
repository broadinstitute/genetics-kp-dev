import connexion
import six

from openapi_server import util


def predicates_get():  # noqa: E501
    """Get supported relationships by source and target

     # noqa: E501


    :rtype: Dict[str, Dict[str, List[str]]]
    """
    predicates = {}
    predicates['disease'] = {}
    predicates['disease']['gene'] = []
    predicates['disease']['gene'].append('associated')
    predicates['disease']['pathway'] = []
    predicates['disease']['pathway'].append('associated')
    predicates['phenotype'] = {}
    predicates['phenotype']['gene'] = []
    predicates['phenotype']['gene'].append('associated')
    predicates['phenotype']['pathway'] = []
    predicates['phenotype']['pathway'].append('associated')
    predicates['gene'] = {}
    predicates['gene']['disease'] = []
    predicates['gene']['disease'].append('associated')
    predicates['gene']['phenotype'] = []
    predicates['gene']['phenotype'].append('associated')
    predicates['pathway'] = {}
    predicates['pathway']['disease'] = []
    predicates['pathway']['disease'].append('associated')
    predicates['pathway']['phenotype'] = []
    predicates['pathway']['phenotype'].append('associated')

    return predicates
