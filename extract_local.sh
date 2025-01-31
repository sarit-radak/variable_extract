#!/bin/bash
# This script extracts the variable regions from the reads. It is designed to be run on a local machine. I use it when Garibaldi is slow and my libraries are small

# Define the input and output directories
input_dir="/Users/sradak/Downloads/25-01-20_A3B2M_S6/files" # input fasta files
pydir="/Users/sradak/Downloads/25-01-20_A3B2M_S6/pythonfiles/"

libraries=("test1" "test2" "test3")
num_regions=6


process_library() {
    local library="$1"

    # export anything written to the terminal into a log file
    log_file="logs/${library}_extract.log"
    exec > "$log_file" 2>&1

    # extract all sequences from fastq directory
    #gunzip $input_dir/*.gz
    python3 $pydir/extract_to_fasta.py $input_dir $library


    # extract the variable regions from each sequence
    python3 -u $pydir"extract.py" "$library" "$num_regions"
}

export -f process_library
export input_dir pydir num_regions

parallel process_library ::: "${libraries[@]}"
