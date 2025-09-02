import pandas as pd
import sys

def calculate_amino_acid_frequencies (input_file, output_file, options):
    # Read the xlsx file
    df = pd.read_csv(input_file)
    
    # pick only the columns with just the variable regions
    valid_cols = [col for col in df.columns[1:] if str(df.iloc[0][col])[0].isupper()]

    # concatenate only those
    sequences = df[valid_cols].agg(''.join, axis=1).tolist()
    

    # create a dictionary to hold the frequencies
    position_frequencies = {}

    all_aminos = ['*', 'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

    # Calculate frequencies
    for seq in sequences:
        for index, amino_acid in enumerate(seq):
            if index not in position_frequencies:
                position_frequencies[index] = {}
            if amino_acid not in position_frequencies[index]:
                position_frequencies[index][amino_acid] = 0
            position_frequencies[index][amino_acid] += 1


    # Convert counts to frequencies
    frequency_rows = []  # List to store each row as a dictionary
    
    for position, amino_acid_counts in position_frequencies.items():
        total_count = sum(amino_acid_counts.values())
        
        # Ensure every amino acid is represented for this position
        for amino_acid in all_aminos:
            count = amino_acid_counts.get(amino_acid, 0)  # Default to 0 if the amino acid isn't found
            frequency_rows.append({
                'Amino Acid': amino_acid,
                'Position': position,
                'Frequency': count / total_count if total_count > 0 else 0  # Avoid division by zero
            })

    # Convert the list of rows to a DataFrame
    frequency_df = pd.DataFrame(frequency_rows, columns=['Amino Acid', 'Position', 'Frequency'])
    
    # Pivot the DataFrame to get positions as columns and amino acids as rows
    pivot_df = frequency_df.pivot(index='Amino Acid', columns='Position', values='Frequency').fillna(0)

    # Read the options file with openpyxl engine
    options_df = pd.read_excel(options, engine='openpyxl')

    # Prepare a new DataFrame to hold the filtered frequencies
    filtered_df = pd.DataFrame(index=pivot_df.index)

    # Check acceptable amino acids against options
    for position in range(pivot_df.shape[1]):
        # Get the acceptable amino acids for this position
        if position < options_df.shape[1]:
            acceptable_amino_acids = options_df.iloc[0, position]
        else:
            acceptable_amino_acids = ''

        # Populate the filtered DataFrame
        filtered_column = []
        for amino_acid in pivot_df.index:
            if amino_acid in acceptable_amino_acids:
                filtered_column.append(pivot_df.at[amino_acid, position])
            else:
                filtered_column.append('')  # Leave blank if not acceptable

        filtered_df[position] = filtered_column
    
    
    # 🔹 Read headers from header_file
    header_df = pd.read_excel("blastdb/sampled_residues.xlsx", engine="openpyxl")
    new_headers = list(header_df.columns)

    # Make sure number of headers matches number of positions
    if len(new_headers) >= filtered_df.shape[1]:
        filtered_df.columns = new_headers[:filtered_df.shape[1]]
    else:
        raise ValueError("Not enough headers in sampled_residues.xlsx to match positions")
    
    filtered_df.to_excel(output_file, index=True)
    
print ("")
print("Calculating amino acid frequency at each position...")

library = sys.argv[1]

input_file = f"files/{library}/{library}.csv"
output_file = f"files/{library}/{library}_freq.xlsx"
options = f"blastdb/sampled_residues.xlsx"

calculate_amino_acid_frequencies (input_file, output_file, options)

print("Frequency calculation complete")
