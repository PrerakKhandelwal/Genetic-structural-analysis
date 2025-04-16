def load_dna_file(file):
    content = file.read().decode("utf-8")
    lines = content.strip().split("\n")
    if lines[0].startswith(">"):
        lines = lines[1:]
    dna = "".join(lines).replace(" ", "").upper()
    return "".join(filter(lambda x: x in "ATCG", dna))


