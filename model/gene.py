from dataclasses import dataclass


@dataclass
class Gene:
    GeneID: str
    Essential: str
    Chromosome: int

    def __str__(self):
        return f"{self.GeneID} | Ess.: {self.Essential}, Chrom.: {self.Chromosome}"

    def __hash__(self):
        return hash(self.GeneID)