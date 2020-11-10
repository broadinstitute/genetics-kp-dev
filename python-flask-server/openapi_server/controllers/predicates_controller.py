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
    predicates['phenotypic_feature'] = {}
    predicates['phenotypic_feature']['gene'] = []
    predicates['phenotypic_feature']['gene'].append('associated')
    predicates['phenotypic_feature']['pathway'] = []
    predicates['phenotypic_feature']['pathway'].append('associated')
    predicates['gene'] = {}
    predicates['gene']['disease'] = []
    predicates['gene']['disease'].append('associated')
    predicates['gene']['phenotypic_feature'] = []
    predicates['gene']['phenotypic_feature'].append('associated')
    predicates['pathway'] = {}
    predicates['pathway']['disease'] = []
    predicates['pathway']['disease'].append('associated')
    predicates['pathway']['phenotypic_feature'] = []
    predicates['pathway']['phenotypic_feature'].append('associated')

    return predicates
