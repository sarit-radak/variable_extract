import pandas as pd
import sys
import re



def calc_fc (lib1, lib2):
    file1 = f"files/{lib1}_freq.xlsx"
    file2 = f"files/{lib2}_freq.xlsx"

    sample1_freq = pd.read_excel(file1, index_col=0, engine='openpyxl')
    sample2_freq = pd.read_excel(file2, index_col=0, engine='openpyxl')

    # Create fc DataFrame with all columns, including the "Amino Acid" column
    fc = sample1_freq.divide(sample2_freq)

    # Handle division by zero or NaN by replacing with an appropriate value (e.g., 0 or NaN)
    fc = fc.fillna(0)  # Replace NaN with 0 (or use other strategies as needed)

    # Re-add the "Amino Acid" column to the fold change dataframe (if not already included)
    #fc.insert(0, "Amino Acid", sample1_freq.index)

    # Extract sample names from filenames
    sample1 = re.search(r'\/(.*?)_freq', file1).group(1)
    sample2 = re.search(r'\/(.*?)_freq', file2).group(1)

    # Save the fold change data to an Excel file
    fc.to_excel(f"files/{sample1}_vs_{sample2}.xlsx", index=True)




lib1 = sys.argv[1]
lib2 = sys.argv[2]
calc_fc (lib1, lib2)