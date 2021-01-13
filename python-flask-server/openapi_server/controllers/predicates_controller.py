import connexion
import six

from openapi_server import util

def predicates_getOld():  # noqa: E501
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

def predicates_get():  # noqa: E501
    """Get supported relationships by source and target

     # noqa: E501


    :rtype: Dict[str, Dict[str, List[str]]]
    """
    predicates = {}
    predicates['biolink:Disease'] = {}
    predicates['biolink:Disease']['biolink:Gene'] = []
    predicates['biolink:Disease']['biolink:Gene'].append('biolink:condition_associated_with_gene')
    predicates['biolink:Disease']['biolink:Pathway'] = []
    predicates['biolink:Disease']['biolink:Pathway'].append('biolink:genetic_association')
    predicates['biolink:PhenotypicFeature'] = {}
    predicates['biolink:PhenotypicFeature']['biolink:Gene'] = []
    predicates['biolink:PhenotypicFeature']['biolink:Gene'].append('biolink:condition_associated_with_gene')
    predicates['biolink:PhenotypicFeature']['biolink:Pathway'] = []
    predicates['biolink:PhenotypicFeature']['biolink:Pathway'].append('biolink:genetic_association')
    predicates['biolink:Gene'] = {}
    predicates['biolink:Gene']['biolink:Disease'] = []
    predicates['biolink:Gene']['biolink:Disease'].append('biolink:gene_associated_with_condition')
    predicates['biolink:Gene']['biolink:PhenotypicFeature'] = []
    predicates['biolink:Gene']['biolink:PhenotypicFeature'].append('biolink:gene_associated_with_condition')
    predicates['biolink:Pathway'] = {}
    predicates['biolink:Pathway']['biolink:Disease'] = []
    predicates['biolink:Pathway']['biolink:Disease'].append('biolink:genetic_association')
    predicates['biolink:Pathway']['biolink:PhenotypicFeature'] = []
    predicates['biolink:Pathway']['biolink:PhenotypicFeature'].append('biolink:genetic_association')

    return predicates
