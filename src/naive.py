"""Implementation of the naive exact matching algorithm."""

import argparse
from parsers import parse_fastq, parse_fasta
from cigar import edits_to_cigar
from align import get_edits


def naive(x: str, p: str) -> list[int]:
    out: list[int] = []
    stop = len(p)
    for i, _ in enumerate(x):
        if x[i:i+stop] == p:
            out.append(i+1)
    return out


def main():
    argparser = argparse.ArgumentParser(
        description="Exact matching using the naive method")
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    args = argparser.parse_args()

    genome = parse_fasta(args.genome)
    reads = parse_fastq(args.reads)
    out = []
    for read in reads:
        for chr in genome:
            hits = naive(genome[chr], reads[read])
            for hit in hits:
                _, _, edit = get_edits(genome[chr][hit:hit+len(reads[read])])
                cigar = edits_to_cigar(edit)
                out.append(
                    f'{read}\t{chr}\t{hit}\t{cigar}\t{reads[read]}')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
