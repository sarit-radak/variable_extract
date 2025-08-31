import sys
import pandas as pd

def calculate_variable_frequency(input_file, output_file):
    df = pd.read_csv(input_file)
    
    variables = df.iloc[:, 1:].agg('_'.join, axis=1)
    
    variable_names = df.columns[1:]    
    
    # count the frequency of each unique variable sequence
    sequence_frequencies = variables.value_counts(normalize=True).sort_values(ascending=False) # Normalize = True for frequencies, False for read counts
    
    
    freq_df = pd.DataFrame(sequence_frequencies).reset_index()
    freq_df.index = freq_df.index + 1
    freq_df.insert(0, "Rank", freq_df.index)
    freq_df.columns = ["Rank", 'Variable Sequence', 'Frequency']
    
    freq_df[variable_names] = freq_df["Variable Sequence"].str.split("_", expand=True)
    
    freq_df = freq_df.drop(columns=["Variable Sequence"])

    freq_df.to_csv(output_file, index=False)
    
print ("")
print("Ranking sequences by frequency...")


library = sys.argv[1]

input_file = f"files/{library}/{library}.csv"
output_file = f"files/{library}/{library}_ranked.csv"

calculate_variable_frequency(input_file, output_file)

print("Ranking complete")