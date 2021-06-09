import json
import requests 
from urllib.error import HTTPError

# constants
# node types
node_gene ='biolink:Gene'
node_disease = 'biolink:Disease'
node_phenotype = 'biolink:PhenotypicFeature'
node_pathway = 'biolink:Pathway'

# edge types
edge_gene_disease = 'biolink:gene_associated_with_condition'
edge_disease_gene = 'biolink:condition_associated_with_gene'
edge_pathway_disease = 'biolink:genetic_association'
edge_disease_pathway = 'biolink:genetic_association'

# attribute types
attribute_pvalue = 'biolink:p_value'
attribute_probability = 'biolink:probability'
attribute_classification = 'biolink:classification'

# list of accepted edge types
accepted_edge_types = [edge_gene_disease, edge_disease_gene, edge_pathway_disease, edge_disease_pathway]

# input type translation map
type_translation_input = {
        # predicates
        'biolink:genetic_association': 'associated',

        # categories
        'biolink:Gene': 'gene',
        'biolink:Disease': 'disease',
        'biolink:PhenotypicFeature': 'phenotypic_feature',
        'biolink:Pathway': 'pathway',
    }

# reverse the type translation map for output
type_translation_output = dict((value, key) for key, value in type_translation_input.items())

# input curie translation map
curie_translation_input = {
        # compounds (biolink: molepro)
        'PUBCHEM.COMPOUND': 'CID',
        'CHEMBL.COMPOUND': 'ChEMBL',
        'DRUGBANK': 'DrugBank',
        'KEGG': 'KEGG.COMPOUND',
    }

# reverse the curie translation map for output
curie_translation_output = dict((value, key) for key, value in curie_translation_input.items())


def translate_type(input_type, is_input=True):
    """ translates the predicates and categories if necessary to/from biolink/molepro """
    result = input_type
    map={}
    if is_input:
        map = type_translation_input
    else:
        map = type_translation_output

    # only translate if necessary
    if input_type in map:
        result = map[input_type]

    # log
    # print("utils.translate_type: returning {} for input {}".format(result, input_type))

    # return
    return result

def translate_curie(input_curie, is_input=True):
    """ translates the curie prefix if necessary to/from biolink/molepro """
    result = input_curie
    map={}
    if is_input:
        map = curie_translation_input
    else:
        map = curie_translation_output

    # split the curie into prefix and value
    if input_curie:
        split_curie = input_curie.split(":")

        if len(split_curie) == 2:
            prefix = split_curie[0]
            value = split_curie[1]

            # if prefix needs to be translated, translate, else leave alone
            if prefix in map:
                result = map[prefix] + ":" + value

    # log
    print("utils.translate_curie: returning {} for input {}".format(result, input_curie))

    # return
    return result

def migrate_transformer_chains(inFile, outFile):
    with open(inFile) as f:
        json_obj = json.load(f)
    for chain in json_obj:
        chain['subject'] = translate_type(chain['subject'], False)
        chain['predicate'] = translate_type(chain['predicate'], False)
        chain['object'] = translate_type(chain['object'], False)
        print(chain['subject'],chain['predicate'],chain['object'],'\n')
    with open(outFile, 'w') as json_file:
        json.dump(json_obj, json_file, indent=4, separators=(',', ': ')) # save to file with prettifying

def get_curie_synonyms(curie_input, prefix_list=None, type_name='', log=False):
    ''' will call the curie normalizer and return the curie name and a list of only the matching prefixes from the prefix list provided '''
    url_normalizer = "https://nodenormalization-sri.renci.org/1.1/get_normalized_nodes?curie={}"
    list_result = []
    curie_name = None

    # log
    if log:
        print("-> get_curie_synonyms got curie {}, ontology lts {} and type name {}".format(curie_input, prefix_list, type_name))

    # if provided no curie, return [None]
    if curie_input is None:
        return curie_name, [None]

    # call the service
    url_call = url_normalizer.format(curie_input)
    response = requests.get(url_call)

    # if error, then return curie input as name and one element array
    if response.status_code == 404:
        curie_name = curie_input
        list_result = [curie_input]
        print("ERROR: got node normalizer error for url: {}".format(url_call))

    else:
        json_response = response.json()

        # get the list of curies
        if json_response.get(curie_input):
            curie_name = json_response.get(curie_input).get('id').get('label')
            for item in json_response[curie_input]['equivalent_identifiers']:
                list_result.append(item['identifier'])

        if log:
            print("got curie synonym list result {}".format(list_result))

    # if a prefix list provided, filter with it
    if prefix_list:
        list_new = []
        for item in list_result:
            if item.split(':')[0] in prefix_list:
                list_new.append(item)
        list_result = list_new

    # return
    # BUG? only return none if none provided
    # list_result = list_result if len(list_result) > 0 else [None]
    if log:
        print("for {} input {} return name {} and ontologies {}\n".format(type_name, curie_input, curie_name, list_result))
    return curie_name, list_result

if (__name__ == "__main__"):
    pass    