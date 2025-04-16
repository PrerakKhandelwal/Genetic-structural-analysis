from utils.translator import translate_rna_to_protein

def find_orfs(rna_seq):
    start_codon = "AUG"
    stop_codons = {"UAA", "UAG", "UGA"}
    orfs = []

    for frame in range(3):
        i = frame
        while i + 3 <= len(rna_seq):
            codon = rna_seq[i:i+3]
            if codon == start_codon:
                j = i + 3
                while j + 3 <= len(rna_seq):
                    stop = rna_seq[j:j+3]
                    if stop in stop_codons:
                        seq = rna_seq[i:j+3]
                        protein = translate_rna_to_protein(seq)
                        orfs.append((i, j+3, protein))
                        break  # Stop at the first in-frame stop codon
                    j += 3
                i = j  # Move index forward to prevent overlapping
            else:
                i += 3
    return orfs
