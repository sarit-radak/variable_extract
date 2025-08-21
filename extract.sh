#!/bin/bash
# make venv (only need to run once)
#python3 -m venv extract
# activate venv
source extract/bin/activate
#python3 -m pip install bio matplotlib openpyxl

mkdir -p logs

libraries=($(find files -mindepth 1 -maxdepth 1 -type d -exec basename {} \;))

# make the blast database
#python3 -u pythonfiles/make_db.py 


for library in "${libraries[@]}"; do
    log_file="logs/${library}_extract.log"
    {
        echo "Processing library: $library"

        # extract sequences to fasta
        #python3 -u pythonfiles/extract_to_fasta.py "$library"

        # extract first 1000 reads
        #awk '/^>/ {count++} count<=1000' files/$library/$library"_all.fasta" >  files/$library/$library"_1000.fasta"
        
        # exclude all reads that aren't long enough
        #python3 -u pythonfiles/sort_by_len.py "$library" 3000

        # blast the reads against the flanking regions
        #python3 -u pythonfiles/blast.py "$library"

        # extract the variable regions from each sequence
        #python3 -u pythonfiles/extract.py "$library"

        # rank the unique sequences
        #python3 -u pythonfiles/rank_var.py "$library"

        # calculate the amino acid frequencies at each position
        python3 -u pythonfiles/calc_freq.py "$library"
    } >"$log_file" 2>&1 &

done

# wait for all backgrounded jobs to finish
wait