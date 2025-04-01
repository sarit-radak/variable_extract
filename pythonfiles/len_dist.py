import sys
import matplotlib.pyplot as plt
from collections import Counter

library = sys.argv[1]
dir = "files/"
input_fasta = f"{dir}{library}_all.fasta"
output_image = f"{dir}{library}_length_distribution.png"

# Function to read FASTA and calculate sequence lengths
def get_length_distribution(fasta_file):
    length_counts = Counter()
    with open(fasta_file, 'r') as f:
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq:
                    length_counts[len(seq)] += 1
                    seq = ""
            else:
                seq += line
        if seq:  # Capture the last sequence
            length_counts[len(seq)] += 1
    return length_counts

# Get length distribution
length_distribution = get_length_distribution(input_fasta)

# Plot and save the histogram
plt.figure(figsize=(10, 6))
plt.bar(length_distribution.keys(), length_distribution.values(), color='skyblue')
plt.xlabel("Sequence Length")
plt.ylabel("Count")
plt.title(f"Length Distribution for {library}")
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig(output_image)

print(f"Length distribution plot saved to {output_image}")
