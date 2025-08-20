#!/bin/bash
# make venv (only need to run once)
#python3 -m venv extract
# activate venv
source extract/bin/activate
#python3 -m pip install bio matplotlib openpyxl

mkdir -p logs
libraries=($(find files -mindepth 1 -maxdepth 1 -type d -exec basename {} \;))



num_regions=3




for library in "${libraries[@]}"; do
    log_file="logs/${library}_extract.log"
    {
        echo "Processing library: $library"

        # extract sequences to fasta
        #python3 -u pythonfiles/extract_to_fasta.py "$library"

        # extract first 1000 reads
        #awk '/^>/ {count++} count<=1000' files/$library"_all.fasta" >  files/$library"_1000.fasta"
        
        # exclude all reads that aren't long enough
        #python3 -u pythonfiles/sort_by_len.py "$library" 3000

        # make the blast database
        #python3 -u pythonfiles/make_db.py "blastdb/flanking_regions.xlsx"

        # blast the reads against the flanking regions
        #python3 -u pythonfiles/blast.py "$library" "$num_regions"

        # extract the variable regions from each sequence
        #python3 -u pythonfiles/extract.py "$library" "$num_regions"

        # rank the unique sequences
        #python3 -u pythonfiles/rank_var.py "$library"


    } >"$log_file" 2>&1 &

done

# wait for all backgrounded jobs to finish
wait

echo yippee




# calculate the amino acid frequencies at each position
#python3 -u pythonfiles/calc_freq.py "$library"

# calculate the fold change between two libraries
#python3 -u pythonfiles/calc_fc.py "test" "test2"
