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

    args = argparser.parse_args()
    genome = parse_fasta(args.genome)
    reads = parse_fastq(args.reads)

    print(time_naive(genome, reads))

    return 0


def time_naive(genome: dict[str, str], reads: dict[str, str]) -> pd.DataFrame:
    n, m, time = [], [], []
    for chr in genome:
        for read in reads:
            print(f"processing {chr} {read}")
            n.append(len(genome[chr]))
            m.append(len(reads[read]))
            cmd = f'naive("{genome[chr]}", "{reads[read]}")'
            print(cmd)
            ti = timeit.timeit(cmd, setup="from naive import naive")
            time.append(ti)
    out = pd.DataFrame({"n size": n, "m size": m, "time": time})
    return out


if __name__ == '__main__':
    main()

sys.exit()


def time_linear():
    n, m, time = [], [], []
    for chr in genome:
        for read in reads:
            n.append(len(genome[chr]))
            m.append(len(reads[read]))
            cmd = f'linear({genome[chr]}, {reads[read]})'
            ti = timeit.timeit(cmd, setup="from lin import linear", number=10)

    ti = timeit.timeit()

    linear()
