import subprocess

command = [
"makeblastdb",
"-in", "blastdb/flanking_regions.fasta",
"-dbtype", "nucl",
"-out", "blastdb/flanking_regions"
]

subprocess.run(command, check=True, stderr=subprocess.DEVNULL)

