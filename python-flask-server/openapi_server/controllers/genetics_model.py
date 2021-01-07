

class GeneticsModel():
    def __init__(self, edge, source, target):
        self.edge = edge
        self.source = source
        self.target = target 
    
    def __str__(self):
        return "edge: {}, source: {}, target: {}".format(self.edge, self.source, self.target)

    __repr__ = __str__
