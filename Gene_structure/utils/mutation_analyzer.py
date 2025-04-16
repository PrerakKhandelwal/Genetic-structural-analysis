from difflib import SequenceMatcher

def compare_proteins(wild_orfs, mutated_orfs):
    output = ""
    for i, (wild, mut) in enumerate(zip(wild_orfs, mutated_orfs)):
        _, _, wild_protein = wild
        _, _, mut_protein = mut
        output += f"### Protein {i+1} Analysis:\n"
        
        # Compare protein sequences
        if wild_protein == mut_protein:
            output += "✅ No changes in amino acid sequence (Silent Mutation)\n"
        else:
            output += "⚠️ Changes detected in amino acid sequence\n"
            
        # Detailed comparison
        sm = SequenceMatcher(None, wild_protein, mut_protein)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != 'equal':
                if tag == 'replace':
                    output += f"- **Amino Acid Change**: Position {i1+1}: `{wild_protein[i1:i2]}` → `{mut_protein[j1:j2]}`\n"
                elif tag == 'delete':
                    output += f"- **Deletion**: Position {i1+1}: Removed `{wild_protein[i1:i2]}`\n"
                elif tag == 'insert':
                    output += f"- **Insertion**: Position {i1+1}: Added `{mut_protein[j1:j2]}`\n"
    
    return output if output else "✅ No mutations found."


