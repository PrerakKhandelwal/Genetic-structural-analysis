nucleotide_weights = {
    'A': 331.2,  # Adenine
    'T': 322.2,  # Thymine
    'C': 307.2,  # Cytosine
    'G': 347.2   # Guanine
}

def calculate_dna_weight(dna_sequence):
    weight = 0
    for nucleotide in dna_sequence:
        weight += nucleotide_weights.get(nucleotide.upper(), 0)
    return weight



def calculate_gc_content(dna_seq: str) -> float:
    dna_seq = dna_seq.upper()
    gc_count = dna_seq.count('G') + dna_seq.count('C')
    total_count = len(dna_seq)
    return (gc_count / total_count) * 100 if total_count > 0 else 0.0