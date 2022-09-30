"""Implementation of a linear time exact matching algorithm."""

import argparse
import sys
from ba import mailund_border_array
from parsers import parse_fasta, parse_fastq
from align import get_edits
from cigar import edits_to_cigar


def lin(x: str, p: str) -> list[int]:
    out: list[int] = []
    n = len(x)
    m = len(p)
    ba = mailund_border_array(p)
    i, j = 0, 0

    while i < n and p:
        while i < n and j < m and x[i] == p[j]:
            if j == m-1 or i == n-1:
                break
            j += 1
            i += 1
        if x[i] == p[j]:
            if i-j > n-m:
                break
            out.append(i - j)
            j = ba[j-1]
        elif j == 0:
            i += 1
        else:
            j = ba[j-1]

    return out


def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching in linear time")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()

    genome = parse_fasta(args.genome)
    reads = parse_fastq(args.reads)
    out = []
    for read in reads:
        for chr in genome:
            hits = lin(genome[chr], reads[read])
            for hit in hits:
                _, _, edit = get_edits(
                    genome[chr][hit:hit+len(reads[read])], reads[read])
                cigar = edits_to_cigar(edit)
                out.append(
                    f'{read}\t{chr}\t{hit+1}\t{cigar}\t{reads[read]}')
    print('\n'.join(out))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("stopped")
        sys.exit()
