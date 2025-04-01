import sys
import subprocess

def blast (library, num_regions):

    blast_command = [
    "blastn",
    "-query", "files/" + library + "_len_pass.fasta",
    "-db", "blastdb/flanking_regions",
    "-out", "files/" + library + "_vs_flanking_regions.txt",
    "-outfmt", "6",
    "-max_target_seqs", str(num_regions*2),
    "-max_hsps", "1",
    "-task", "blastn-short" # this arguement is critical for the search to successfully identify the correct alignments. I think it adjusts the gap penalties and scoring matricies to values that are optimized for searches with small sequences.
    ]
    
    subprocess.run(blast_command, check=True, stderr=subprocess.DEVNULL)



library = sys.argv[1]
num_regions = int(sys.argv[2])


fasta_file = f"files/{library}_len_pass.fasta" # fasta file of reads

print (f"blasting {library} against flanking regions")
blast (library, num_regions)

