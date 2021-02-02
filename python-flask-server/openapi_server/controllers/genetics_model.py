

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


class QueryInput():
    ''' class to return objects of the query graph '''
    def __init__(self, edge, source, target):
        self.edge = edge
        self.source = source
        self.target = target 
    
    def __str__(self):
        return "edge: {}, source: {}, target: {}".format(self.edge, self.source, self.target)

    __repr__ = __str__

    def get_edge_key(self):
        return self.edge.get('edge_key')

    def get_edge_type(self):
        return self.edge.get('predicate')

    def get_source_id(self):
        return self.source.get('id')

    def get_source_node_key(self):
        return self.source.get('node_key')

    def get_source_type(self):
        return self.source.get('category')
    
    def get_target_node_key(self):
        return self.target.get('node_key')

    def get_target_type(self):
        return self.target.get('category')

    def get_target_id(self):
        return self.target.get('id')

    def is_disease_gene_query(self):
        return (self.get_source_type() == node_disease or self.get_source_type() == node_phenotype) and self.get_target_type() == node_gene and self.get_edge_type() == edge_disease_gene

    def is_disease_pathway_query(self):
        return (self.get_source_type() == node_disease or self.get_source_type() == node_phenotype) and self.get_target_type() == node_pathway and self.get_edge_type() == edge_disease_pathway

    def is_pathway_disease_query(self):
        return self.get_source_type() == node_pathway and (self.get_target_type() == node_disease or self.get_target_type() == node_phenotype) and self.get_edge_type() == edge_pathway_disease

    def is_gene_disease_query(self):
        return self.get_source_type() == node_gene and (self.get_target_type() == node_disease or self.get_target_type() == node_phenotype) and self.get_edge_type() == edge_gene_disease


class NodeOuput():
    ''' class to encapsulate result nodes '''
    def __init__(self, curie, name, category, node_key):
        self.curie = curie
        self.name = name
        self.category = category
        self.node_key = node_key 
    
    def __str__(self):
        return "curie: {}, name: {}, category: {}, node key: {}".format(self.curie, self.name, self.category, self.node_key)

    __repr__ = __str__
        
class EdgeOuput():
    ''' class to encapsulate the result edges '''
    def __init__(self, id, source_node, target_node, predicate, edge_key, score=None, score_type=None):
        self.id = id
        self.source_node = source_node
        self.target_node = target_node
        self.predicate = predicate
        self.score = score 
        self.score_type = score_type
        self.edge_key = edge_key
    
    def __str__(self):
        return "id: {}, subject: {}, object: {}, perdicate: {}, edge key: {}, score: {}, score type: {}".format(self.id, self.source_node, self.target_node, self.predicate, self.edge_key, self.score, self.score_type)

    __repr__ = __str__

