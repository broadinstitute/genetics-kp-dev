

class GeneticsModel():
    def __init__(self, edge, source, target):
        self.edge = edge
        self.source = source
        self.target = target 
    
    def __str__(self):
        return "edge: {}, source: {}, target: {}".format(self.edge, self.source, self.target)

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

