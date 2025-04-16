import streamlit as st
from utils.file_handler import load_dna_file
from utils.transcriber import transcribe_dna_to_rna
from utils.orf_scanner import find_orfs
from utils.mutation_analyzer import compare_proteins
from utils.gc_calculator import calculate_gc_content

# Define nucleotide weights (in g/mol or another suitable unit)
nucleotide_weights = {
    'A': 331.2,  # Adenine
    'T': 322.2,  # Thymine
    'C': 307.2,  # Cytosine
    'G': 347.2   # Guanine
}

# Function to calculate the weight of a DNA sequence
def calculate_dna_weight(dna_sequence):
    weight = sum(nucleotide_weights.get(n.upper(), 0) for n in dna_sequence)
    return weight

# Streamlit Page Setup
st.set_page_config(page_title="GENE-STRUCT", layout="wide")
st.title("🧬 GENE-STRUCT: DNA → Protein Explorer")

uploaded_file = st.file_uploader("Upload a DNA sequence file (.txt or .fasta)", type=["txt", "fasta"])

if uploaded_file:
    dna_seq = load_dna_file(uploaded_file)
    st.subheader("📄 Input DNA Sequence")
    st.code(dna_seq)

    gc_original = calculate_gc_content(dna_seq)
    st.metric("🧪 GC Content (Original DNA)", f"{gc_original:.2f}%")

    original_weight = calculate_dna_weight(dna_seq)
    st.metric("🧪 Weight of Original DNA Sequence", f"{original_weight:.2f} g/mol")

    rna_seq = transcribe_dna_to_rna(dna_seq)
    st.subheader("🔁 Transcribed RNA Sequence")
    st.code(rna_seq)

    orfs = find_orfs(rna_seq)
    st.subheader("🧬 Translated Protein(s) from ORFs")
    if orfs:
        for i, (start, stop, protein) in enumerate(orfs):
            st.markdown(f"### Protein {i+1}")
            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.markdown("**Position Information:**")
                    st.markdown(f"- Start: `{start}`")
                    st.markdown(f"- Stop: `{stop}`")
                    st.markdown(f"- Length: `{len(protein)}` amino acids")
                with col2:
                    st.markdown("**Protein Sequence:**")
                    formatted_protein = ' '.join([protein[i:i+10] for i in range(0, len(protein), 10)])
                    st.code(formatted_protein)

                    st.markdown("**Amino Acid Composition:**")
                    aa_composition = {}
                    for aa in protein:
                        aa_composition[aa] = aa_composition.get(aa, 0) + 1
                    composition_text = ', '.join([f"{aa}: {count}" for aa, count in sorted(aa_composition.items())])
                    st.markdown(composition_text)
    else:
        st.warning("No valid ORFs found in the RNA sequence.")

    if st.checkbox("🧪 Compare with Mutated DNA"):
        mutated_file = st.file_uploader("Upload Mutated DNA File", type=["txt", "fasta"])
        if mutated_file:
            mut_dna = load_dna_file(mutated_file)
            st.subheader("🧬 Mutated DNA Sequence")
            st.code(mut_dna)

            gc_mut = calculate_gc_content(mut_dna)
            st.metric("🧬 GC Content (Mutated DNA)", f"{gc_mut:.2f}%")

            mutated_weight = calculate_dna_weight(mut_dna)
            st.metric("🧬 Weight of Mutated DNA Sequence", f"{mutated_weight:.2f} g/mol")

            if gc_mut > gc_original:
                st.success("🧬 Mutated DNA is more evolved (higher GC content)")
            elif gc_mut < gc_original:
                st.warning("🐒 Mutated DNA appears more primitive (lower GC content)")
            else:
                st.info("🧬 Both sequences have equal GC content.")

            mut_rna = transcribe_dna_to_rna(mut_dna)
            mut_orfs = find_orfs(mut_rna)

            st.subheader("🔍 Mutation Analysis")

            st.markdown("### DNA Sequence Differences")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original DNA:**")
                st.code(dna_seq)
            with col2:
                st.markdown("**Mutated DNA:**")
                st.code(mut_dna)

            st.markdown("### RNA Sequence Differences")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Original RNA:**")
                st.code(rna_seq)
            with col2:
                st.markdown("**Mutated RNA:**")
                st.code(mut_rna)

            st.markdown("### Protein Sequence Differences")
            result = compare_proteins(orfs, mut_orfs)
            st.markdown(result)

            for i in range(min(len(dna_seq), len(mut_dna))):
                if dna_seq[i] != mut_dna[i]:
                    st.markdown(f"**Mutation found at position {i+1}:**")
                    st.markdown(f"- Original: `{dna_seq[i]}` → Mutated: `{mut_dna[i]}`")
                    st.markdown(f"- This affects codon: `{rna_seq[i:i+3]}` → `{mut_rna[i:i+3]}`")

            st.markdown("### Mutated Proteins")
            if mut_orfs:
                for i, (start, stop, protein) in enumerate(mut_orfs):
                    st.markdown(f"### Mutated Protein {i+1}")
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.markdown("**Position Information:**")
                            st.markdown(f"- Start: `{start}`")
                            st.markdown(f"- Stop: `{stop}`")
                            st.markdown(f"- Length: `{len(protein)}` amino acids")
                        with col2:
                            st.markdown("**Protein Sequence:**")
                            formatted_protein = ' '.join([protein[i:i+10] for i in range(0, len(protein), 10)])
                            st.code(formatted_protein)

                            st.markdown("**Amino Acid Composition:**")
                            aa_composition = {}
                            for aa in protein:
                                aa_composition[aa] = aa_composition.get(aa, 0) + 1
                            composition_text = ', '.join([f"{aa}: {count}" for aa, count in sorted(aa_composition.items())])
                            st.markdown(composition_text)
            else:
                st.warning("No valid ORFs found in the mutated RNA sequence.")
