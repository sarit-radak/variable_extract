# This script adds a folder in each fastq folder with its name. I do this just in case I mess up the barcode deconvolution or want to check my work.

#!/bin/bash

#SBATCH --job-name=Rename
#SBATCH --output=logs/misc/%x%A_%a.out # redirects out files
#SBATCH --error=logs/misc/%x%A_%a.err # redirects error files
#SBATCH --array=1
#SBATCH --time=7-00:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=16GB


# Define the input and output directories
input_dir="/Users/sradak/Downloads/Variable_Extract/files" # input fasta files
pydir="/Users/sradak/Downloads/Variable_Extract/pythonfiles/"

# add a file with the name of the barcode to each fastq folder
for folder in files/*/; do
    #Remove the trailing slash from the folder name
    old_name="${folder%/}"
  
    # Create a text file inside the folder with the old folder name
    echo "$old_name" > "${folder}old_name.txt"  
done

# To rename folders, use "mv old_name new_name"