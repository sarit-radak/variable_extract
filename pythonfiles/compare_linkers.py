'''
This code counts the length of each variable region named "Linker" in each library. It then summarizes the lengths in a file called "linker_lengths.xlsx"

Call it in a bash file using:
python3 -u $pydir"compare_linkers.py" "${libraries[@]}"

'''

import sys
import pandas as pd
from collections import Counter

def get_linker_lengths(library):
    input_file = f"files/{library}.csv"
    # Read the CSV file into a DataFrame
    sequences = pd.read_csv(input_file)
    
    lengths = []

    # Iterate over the rows to calculate the lengths of the Linker column
    for row in sequences.itertuples(index=False):
        lengths.append(len(row.Linker))

    # Count the frequencies of the linker lengths
    length_counts = Counter(lengths)
    
    # Define the fixed order for the output
    fixed_order = ["Library", '12', '13', '14', "15", "16"]
    
    # Prepare the new row for the summary
    new_row = {"Library": library}
    new_row.update({
        status: length_counts.get(int(status), 0)  # Convert 'status' to int since lengths are integers
        for status in fixed_order if status != "Library"
    })

    return new_row


libraries = sys.argv[1:]

columns = ["Library", '12', '13', '14', "15", "16"]
df = pd.DataFrame(columns=columns)
for library in libraries:

    row = get_linker_lengths (library)
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)

df.to_excel("files/linker_lengths.xlsx")