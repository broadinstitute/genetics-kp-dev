from openapi_server.dcc.utils import get_logger

# get logger
logger = get_logger(__name__)

class GeneticsModel():
    ''' class to encapsulate the web query object values '''
    def __init__(self, edge, source, target, list_source_id=None, list_target_id=None, map_source_normalized_id={}, map_target_normalized_id={}, edge_type=None, source_type=None, target_type=None):
        self.edge = edge
        self.source = source
        self.target = target 
        self.list_source_id = list_source_id 
        self.list_target_id = list_target_id 
        self.edge_type = edge_type
        self.source_type = source_type
        self.target_type = target_type
        self.map_source_normalized_id = map_source_normalized_id
        self.map_target_normalized_id = map_target_normalized_id
        # logger.info("created {} with source {} and target {}\n".format(edge, source, target))

    def get_edge(self):
        return self.edge

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_edge_type(self):
        return self.edge_type

    def get_source_type(self):
        return self.source_type

    def get_target_type(self):
        return self.target_type

    def get_edge_types(self):
        return self.edge.get('predicates')

    def get_source_types(self):
        return self.source.get('categories')

    def get_target_types(self):
        return self.target.get('categories')

    def get_original_source_ids(self):
        return self.source.get('ids')

    def get_list_source_id(self):
        # return self.list_source_id
        return list(self.map_source_normalized_id.keys())

    def get_map_source_normalized_id(self):
        return self.map_source_normalized_id

    def add_source_normalized_id(self, key, value):
        logger.info("adding source {} - {}".format(key, value))
        self.map_source_normalized_id[key] = value

    def get_map_target_normalized_id(self):
        return self.map_target_normalized_id

    def add_target_normalized_id(self, key, value):
        logger.info("adding target {} - {}".format(key, value))
        self.map_target_normalized_id[key] = value

    def get_original_target_ids(self):
        return self.target.get('ids')

    def get_list_target_id(self):
        # return self.list_target_id
        return list(self.map_target_normalized_id.keys())

    def get_edge_key(self):
        return self.edge.get('edge_key')

    def get_source_key(self):
        return self.source.get('node_key')

    def get_target_key(self):
        return self.target.get('node_key')
    
  
    def __str__(self):
        return "edge: {}, source: {}, target: {}, map source: {}, map target: {}".format(self.edge, self.source, self.target, self.map_source_normalized_id, self.map_target_normalized_id)

    __repr__ = __str__



class NodeOuput():
    def __init__(self, curie, name, category, node_key):
        self.curie = curie
        self.name = name
        self.category = category
        self.node_key = node_key 
    
    def __str__(self):
        return "curie: {}, name: {}, category: {}, node key: {}".format(self.curie, self.name, self.category, self.node_key)

    __repr__ = __str__
        
class EdgeOuput():
    def __init__(self, id, source_node, target_node, predicate, edge_key, study_type_id, score=None, score_type=None, publication_ids=None, score_translator=None):
        self.id = id
        self.source_node = source_node
        self.target_node = target_node
        self.predicate = predicate
        self.score = score 
        self.score_type = score_type
        self.edge_key = edge_key
        self.study_type_id = study_type_id
        self.publication_ids = publication_ids
        self.score_translator = score_translator
    
    def __str__(self):
        return "id: {}, subject: {}, object: {}, perdicate: {}, edge key: {}, score: {}, score type: {}, study: {}".format(self.id, self.source_node, self.target_node, self.predicate, self.edge_key, self.score, self.score_type, self.study_type_id)

    __repr__ = __str__

