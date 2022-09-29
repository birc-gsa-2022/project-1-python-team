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

    lin = time_linear(genome, reads)
    naive = time_naive(genome, reads)
    out = pd.concat((lin, naive["naive time"]), 1)
    out.to_csv("out_table.csv", index=False)

    return 0


def time_naive(genome: dict[str, str], reads: dict[str, str]) -> pd.DataFrame:
    n, m, time = [], [], []
    for chr in genome:
        for read in reads:
            print(f"processing {chr} {read}")
            n.append(len(genome[chr]))
            m.append(len(reads[read]))
            cmd = f'naive("{genome[chr]}", "{reads[read]}")'
            ti = timeit.timeit(
                cmd, setup="from naive import naive", number=100)
            time.append(ti)
    out = pd.DataFrame({"n size": n, "m size": m, "naive time": time})
    return out


def time_linear(genome: dict[str, str], reads: dict[str, str]) -> pd.DataFrame:
    n, m, time = [], [], []
    for chr in genome:
        for read in reads:
            print(f"processing {chr} {read}")
            n.append(len(genome[chr]))
            m.append(len(reads[read]))
            cmd = f'lin("{genome[chr]}", "{reads[read]}")'
            ti = timeit.timeit(cmd, setup="from lin import lin", number=100)
            time.append(ti)
    out = pd.DataFrame({"n size": n, "m size": m, "linear time": time})
    return out


if __name__ == '__main__':
    main()
