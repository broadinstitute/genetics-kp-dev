

class CreativeNode:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class CreativeEdge:
    def __init__(self, subject, target, score):
        self.subject = subject
        self.target = target
        self.score = score

class CreativeResult:
    def __int__(self, gene, pathway, disease, drug, pathway_gene, gene_disease, pathway_disease, drug_gene):
        self.gene = gene
        self.disease = disease
        self.pathway = pathway
        self.drug = drug
        self.pathway_gene = pathway_gene
        self.pathway_disease = pathway_disease
        self.gene_disease = gene_disease
        self.drug_gene = drug_gene



