#!/bin/bash
# This script extracts the variable regions from the reads. It is designed to be run on Garibaldi

#SBATCH --job-name=Extract_Test
#SBATCH --array=1-1 # one array for each library
#SBATCH --time=7-00:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=16GB

# get directory names
if [[ -n "$SLURM_SUBMIT_DIR" ]]; then
    # Running under SLURM
    cd "$SLURM_SUBMIT_DIR" || exit 1
    dir="$SLURM_SUBMIT_DIR"
    
    input_dir="$dir/files/"
    pydir="$dir/pythonfiles/"

else
    # Running interactively with bash
    dir="$(realpath $(dirname "${BASH_SOURCE[0]}"))"
    input_dir="$dir/files/"
    pydir="$dir/pythonfiles/"
fi


libraries=("test")
library=${libraries[$((SLURM_ARRAY_TASK_ID-1))]}
num_regions=3

# export anything written to the terminal into a log file
log_file="logs/${library}_extract.log"
exec > "$log_file" 2>&1


# extract sequences to fasta
python3 -u $pydir"extract_to_fasta.py" "$library"

# calculate length distribution
python3 -u $pydir"len_dist.py" "$library"

min_len=3000

# exclude all reads that aren't long enough
#python3 -u $pydir"sort_by_len.py" "$library" "$min_len"

# make the blast database
#python3 -u $pydir"make_db.py" "${dir}/blastdb/flanking_regions.xlsx"

# blast the reads against the flanking regions
#python3 -u $pydir"blast.py" "$library" "$num_regions"

# extract the variable regions from each sequence
#python3 -u $pydir"extract.py" "$library" "$num_regions"

# rank the unique sequences
#python3 -u $pydir"rank_var.py" "$library"

# calculate the amino acid frequencies at each position
#python3 -u $pydir"calc_freq.py" "$library"

# calculate the fold change between two libraries
#python3 -u $pydir"calc_fc.py" "test" "test2"