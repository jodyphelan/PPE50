import argparse
import subprocess as sp
from tempfile import NamedTemporaryFile
import pysam

argparser = argparse.ArgumentParser(description='Extract PPE from PGAP output')
argparser.add_argument('-s', '--subject', required=True, help='PGAP output file')
argparser.add_argument('-q', '--query', required=True, help='PGAP output file')
argparser.add_argument('-o', '--output', required=True, help='Output file')
argparser.add_argument('-n', '--name', required=True, help='Output file')
argparser.add_argument('-i', '--identity', default=95, help='Output file')
argparser.add_argument('-m', '--matches', default=100, help='Output file')
args = argparser.parse_args()

hits = []
with NamedTemporaryFile('w+t') as tmpfile:
    sp.run(f"blastp -subject {args.subject} -query {args.query}  -outfmt 6 > {tmpfile.name}", shell=True)
    for line in tmpfile:
        row = line.split()
        if float(row[2]) >= args.identity and int(row[3]) >= args.matches:
            hits.append(row[1])

print(f"Found {len(hits)} hits")
print(hits)
with open(args.output, 'w') as outfile:
    fasta = pysam.FastaFile(args.subject)
    for hit in hits:
        outfile.write(f">{args.name}\n{fasta.fetch(hit)}\n")
