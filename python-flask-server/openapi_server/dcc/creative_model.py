

class CreativeNode:
    def __init__(self, id, name, category, query_node_binding_key, prefix):
        self.id = id
        self.name = name
        self.category = category
        self.prefix = prefix
        self.query_node_binding_key = query_node_binding_key

class CreativeEdge:
    def __init__(self, row_id, subject, target, predicate, score):
        self.subject: CreativeNode = subject
        self.target: CreativeNode = target
        self.predicate = predicate
        self.score = score
        self.query_edge_binding_key = subject.prefix + '_' + target.prefix
        self.edge_id = str(row_id) + '_' + subject.id + '_' + target.id

class CreativeResult:
    def __init__(self, row_id, gene, pathway, disease, drug, pathway_gene, gene_disease, pathway_disease, drug_gene):
        self.row_id = row_id
        self.gene: CreativeNode = gene
        self.disease: CreativeNode = disease
        self.pathway: CreativeNode = pathway
        self.drug: CreativeNode = drug
        self.pathway_gene: CreativeEdge = pathway_gene
        self.pathway_disease: CreativeEdge = pathway_disease
        self.gene_disease: CreativeEdge = gene_disease
        self.drug_gene: CreativeEdge = drug_gene

        self.list_edges = [pathway_gene, gene_disease, pathway_disease, drug_gene]
        self.list_nodes = [gene, pathway, disease, drug]

