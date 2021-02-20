import json

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
    print("utils.translate_type: returning {} for input {}".format(result, input_type))

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

if (__name__ == "__main__"):
    curie = "ChEMBL:CHEMBL1197118"
    translated_curie = translate_curie(curie, False)

    migrate_transformer_chains("transformer_chains.json","transformer_chains.json")
