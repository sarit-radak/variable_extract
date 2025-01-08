#!/bin/bash

#SBATCH --job-name=Extract_Test
#SBATCH --output=logs/misc/%x%A_%a.out # redirects out files
#SBATCH --error=logs/misc/%x%A_%a.err # redirects error files
#SBATCH --array=1-4 # one array for each library
#SBATCH --time=7-00:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=16GB


# Define the input and output directories
input_dir="/Users/sradak/Downloads/24-12-12_Variable_Extract/files" # input fasta files
pydir="/Users/sradak/Downloads/24-12-12_Variable_Extract/pythonfiles/"

libraries=("test")
num_regions=1



library=${libraries[$((SLURM_ARRAY_TASK_ID-1))]}
# export anything written to the terminal into a log file
log_file="logs/${library}_extract.log"
exec > "$log_file" 2>&1

# extract the variable regions from each sequence
python3 -u $pydir"extract.py" "$library" "$num_regions"
