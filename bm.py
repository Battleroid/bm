"""
Usage:
    bm-sample.py [options] <input>

Options:
    -h --help  Show this screen.
"""

from docopt import docopt
import pandas as pd


def lookup_table(df, a, b):
    raise NotImplementedError


def he_pair(df, a, b):
    combined = pd.concat([df[a], df[b]])
    freqs = [pow(float(x) / len(combined), 2)
            for x in combined.value_counts()]
    return 1 - sum(freqs)


def main(args):
    # load
    df = pd.read_csv(args['<input>']) 
    df_p = pd.DataFrame(data=None, columns=df.columns)

    # setup pairs
    locii_cols = df.filter(like='Locus').columns
    nr_cols = df.filter(like='NR').columns
    lnr_pairs = zip(locii_cols, nr_cols)

    # calculate baseline He
    baseline_he = sum([he_pair(df, a, b) for a, b in lnr_pairs]) / len(lnr_pairs)

    # master lookup tables


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
