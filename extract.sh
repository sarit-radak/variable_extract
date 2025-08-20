#!/bin/bash

# ===== SLURM directives (ignored locally) =====
#SBATCH --job-name=Extract_Test
#SBATCH --output=logs/misc/%x%A_%a.out
#SBATCH --error=logs/misc/%x%A_%a.err
#SBATCH --array=1-1
#SBATCH --time=7-00:00:00
#SBATCH --cpus-per-task=16
#SBATCH --mem=16GB

# ===== Define libraries =====
libraries=("test")

# if SLURM_ARRAY_TASK_ID is missing, default to first element
if [[ -n "$SLURM_ARRAY_TASK_ID" ]]; then
    library=${libraries[$((SLURM_ARRAY_TASK_ID-1))]}
else
    library=${libraries[0]}
fi

num_regions=3

echo "Running on library: $library"


# ===== Parallel execution =====
# Example: run a python script in parallel across regions
# locally use GNU parallel or xargs
regions=$(seq 1 $num_regions)

if [[ -n "$SLURM_CPUS_PER_TASK" ]]; then
    cpus=$SLURM_CPUS_PER_TASK
else
    cpus=$(sysctl -n hw.ncpu)   # detect CPU cores on Mac
fi

export library input_dir pydir
echo "$regions" | xargs -n 1 -P "$cpus" -I {} \
    echo ligma
    #python3 "$pydir/extract_regions.py" --library "$library" --region {}














# export anything written to the terminal into a log file
#log_file="logs/${library}_extract.log"
#exec > "$log_file" 2>&1

# extract sequences to fasta
#python3 -u $pydir"extract_to_fasta.py" "$library"

# calculate length distribution
#python3 -u $pydir"len_dist.py" "$library"

#min_len=3000

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
