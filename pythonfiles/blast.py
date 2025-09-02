import sys
import time
import subprocess
import pandas as pd

def blast (library, num_regions):

    blast_command = [
    "blastn",
    "-query", "files/" + library + "/" + library + "_len_pass.fasta",
    "-db", "blastdb/flanking_regions",
    "-out", "files/" + library + "/" + library + "_vs_flanking_regions.txt",
    "-outfmt", "6",
    "-max_target_seqs", str(num_regions*2),
    "-max_hsps", "1",
    "-task", "blastn-short" # this arguement is critical for the search to successfully identify the correct alignments. Tt adjusts the gap penalties and scoring matricies to values that are optimized for searches with small sequences.
    ]
    
    subprocess.run(blast_command, check=True, stderr=subprocess.DEVNULL)

def format_elapsed(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds*1000:.0f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        m, s = divmod(seconds, 60)
        return f"{int(m)}m {s:.1f}s"
    else:
        h, rem = divmod(seconds, 3600)
        m, s = divmod(rem, 60)
        return f"{int(h)}h {int(m)}m {s:.0f}s"

print ("")
print("BLASTing against flanking regions...")


library = sys.argv[1]

df = pd.read_excel("config.xlsx")
df = df[df["Variable/Constant"].str.lower() == "variable"]
num_regions = len(df)


start = time.time()
blast(library, num_regions)
end = time.time()

elapsed = end - start
print(f"BLAST complete in {format_elapsed(elapsed)}")