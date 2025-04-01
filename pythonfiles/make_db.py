import sys
import subprocess
import pandas as pd

excel_file = sys.argv[1]
fasta_file = excel_file.replace(".xlsx", ".fasta")


def convert_to_fasta(input_file, output_file):
    # Read the data
    df = pd.read_excel(input_file)

    # Open the output file for writing
    with open(output_file, 'w') as fasta_file:
        # Loop over each row in the dataframe
        for index, row in df.iterrows():
            name = row['Name']
            length = row['Length']
            strand = row["Strand"]
            five_prime = row['5\' Flanking Region']
            three_prime = row['3\' Flanking Region']
            
            # Write the 5' region
            if strand == "Top":
                fasta_file.write(f">{name}_5prime-{length}\n")
            elif strand == "Bottom":
                fasta_file.write(f">{name}_5prime-{length}-R\n")
            else:
                print ("Strand is neither Top or Bottom")
            fasta_file.write(f"{five_prime}\n")
            
            # Write the 3' region
            fasta_file.write(f">{name}_3prime\n")
            fasta_file.write(f"{three_prime}\n")            

convert_to_fasta(excel_file, fasta_file)



command = [
"makeblastdb",
"-in", "blastdb/flanking_regions.fasta",
"-dbtype", "nucl",
"-out", "blastdb/flanking_regions"
]

subprocess.run(command, check=True, stderr=subprocess.DEVNULL)

