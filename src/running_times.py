from secrets import choice
import sys
import timeit
import pandas as pd
import argparse
from parsers import parse_fasta, parse_fastq


def main():
    argparser = argparse.ArgumentParser(
        description="Test script for testing running times of pattern matching algs")
    #argparser.add_argument("test_data", type=pathlib.Path)
    argparser.add_argument("genome", type=argparse.FileType('r'))
    argparser.add_argument("reads", type=argparse.FileType('r'))
    argparser.add_argument("-o", "--outfile", type=str, default="out_table")
    argparser.add_argument("-r", "--runs", type=int, default=10)

    args = argparser.parse_args()
    genome = parse_fasta(args.genome)
    reads = parse_fastq(args.reads)

    lin = time_linear(genome, reads, args.runs)
    naive = time_naive(genome, reads, args.runs)
    out = pd.concat((lin, naive["naive time"]), 1)
    out.to_csv(f'{args.outfile}.csv', index=False)

    return 0


def time_naive(genome: dict[str, str], reads: dict[str, str], runs: int) -> pd.DataFrame:
    n, m, time = [], [], []
    for i, chr in enumerate(genome):
        for j, read in enumerate(reads):
            if i == j:
                print(f"processing naive seq: {chr}, read: {read}")
                n.append(len(genome[chr]))
                m.append(len(reads[read]))
                cmd = f'naive("{genome[chr]}", "{reads[read]}")'
                ti = timeit.timeit(
                    cmd, setup="from naive import naive", number=runs)
                time.append(ti)
    out = pd.DataFrame({"n size": n, "m size": m, "naive time": time})
    return out


def time_linear(genome: dict[str, str], reads: dict[str, str], runs: int) -> pd.DataFrame:
    n, m, time = [], [], []
    for i, chr in enumerate(genome):
        for j, read in enumerate(reads):
            if i == j:
                print(f"processing linear seq: {chr}, read: {read}")
                n.append(len(genome[chr]))
                m.append(len(reads[read]))
                cmd = f'lin("{genome[chr]}", "{reads[read]}")'
                ti = timeit.timeit(
                    cmd, setup="from lin import lin", number=runs)
                time.append(ti)
    out = pd.DataFrame({"n size": n, "m size": m, "linear time": time})
    return out


if __name__ == '__main__':
    main()
