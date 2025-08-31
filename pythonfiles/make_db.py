import sys
import subprocess
import pandas as pd

excel_file = "config.xlsx"
fasta_file = "blastdb/flanking_regions.fasta"



def make_sampled_residues_file(excel_file):
    # output file
    output_file = "blastdb/sampled_residues.xlsx"

    ALL_AAS = "*ACDEFGHIKLMNPQRSTVWY"

    df = pd.read_excel(excel_file)
    df = df[df["Variable/Constant"].str.lower() == "variable"]
    expanded = {}

    for _, row in df.iterrows():
        protein = row["Protein"]
        start_pos = int(row["Start Position"])
        length = int(row["Length"])

        wt_residues = str(row["WT Residue"]).split(":") if pd.notna(row["WT Residue"]) else []
        sampled_residues = str(row["Sampled Residues"]).split(":") if pd.notna(row["Sampled Residues"]) else []

        for i in range(length):
            pos = start_pos + i
            wt = wt_residues[i] if i < len(wt_residues) else "X"
            col_name = f"{protein} {wt}{pos}"

            if i < len(sampled_residues) and sampled_residues[i] != "":
                expanded[col_name] = sampled_residues[i]
            else:
                expanded[col_name] = ALL_AAS

    out_df = pd.DataFrame([expanded])

    ordered_cols = list(expanded.keys())
    out_df = out_df[ordered_cols]

    out_df.to_excel(output_file, index=False)

def name_make(row):
    row['Protein'] = row['Protein'].replace(" ", "_")

    if row["Length"] == 1:
        return row['Protein'] + "_" + str(int(row["Start Position"]))
    else:
        return row['Protein'] + "_" + str(int(row["Start Position"])) + "_" + str (int (row["Start Position"]) + int (row["Length"]) - 1)

def convert_to_fasta(input_file, output_file):
    # Read the data
    df = pd.read_excel(input_file)
    df = df[df["Variable/Constant"].str.lower() == "variable"]

    with open(output_file, 'w') as fasta_file:
        for index, row in df.iterrows():
            
            name = name_make(row)
            length = int(row['Length'])
            strand = row["Strand"]
            five_prime = row['5\' Flanking Region']
            three_prime = row['3\' Flanking Region']
            
            if strand == "Top":
                fasta_file.write(f">{name}-5prime-{length}\n")
            elif strand == "Bottom":
                fasta_file.write(f">{name}-5prime-{length}-R\n")
            else:
                print ("Strand is neither Top or Bottom")
            fasta_file.write(f"{five_prime}\n")
            
            fasta_file.write(f">{name}-3prime\n")
            fasta_file.write(f"{three_prime}\n")            

def count_fasta_sequences(fasta_file):
    with open(fasta_file) as f:
        return sum(1 for line in f if line.startswith(">"))



make_sampled_residues_file(excel_file)
print(f"Sampled residues written to blastdb/sampled_residues.xlsx")



# convert flanking regions to fasta file for building database
convert_to_fasta(excel_file, fasta_file)

command = [
"makeblastdb",
"-in", "blastdb/flanking_regions.fasta",
"-dbtype", "nucl",
"-out", "blastdb/flanking_regions"
]

subprocess.run(
    command,
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL
)

print (f"BLAST database written to blastdb/flanking_regions with {count_fasta_sequences(fasta_file)} sequences")
