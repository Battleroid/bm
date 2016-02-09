"""
Usage:
    bm-sample.py [options] <input>

Options:
    -h --help  Show this screen.
"""

import random
from docopt import docopt
import pandas as pd
import numpy as np


def lookup_table(df, a, b):
    lookup = pd.concat([df[a], df[b]]) \
            .value_counts()\
            .reset_index()
    lookup.columns = ['value', 'freq']
    lookup.sort_values(['value'], inplace=True)
    lookup.index = lookup.value
    lookup = lookup.reindex(np.arange(lookup.value.min(), 
        lookup.value.max() + 1), fill_value=0)
    lookup.index.name = 'idx'
    return lookup


def lookup_new_he(tbl, kill):
    key = tbl.iloc[0].value # lowest value in lookup table
    tmp = tbl.copy()
    for n in kill:
        tmp.freq.iloc[int(n) - key] -= 1
    he = he_lookup(tmp)
    return tmp, he


def he_lookup(tbl):
    he = tbl.freq.divide(tbl.freq.sum())\
            .apply(lambda x: pow(x, 2))\
            .sum()
    return 1 - he


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
    baseline_he = sum([he_pair(df, a, b) for 
        a, b in lnr_pairs]) / len(lnr_pairs)
    print 'Baseline He:', baseline_he

    # generate master lookup tables
    lookups = []
    for locus, nr in lnr_pairs:
        lookups.append(lookup_table(df, locus, nr))

    # being process of random selection
    df_prime = pd.DataFrame(data=None, columns=df.columns, index=df.index)\
            .dropna()
    done = False
    while not done or len(df) == 0:

        # pick random row
        row = df.ix[random.sample(df.index, 1)]

        # calculate temporary He for comparison
        tentative_he = 0
        tmp_lookups = []
        for i, lk in enumerate(lookups):
            l = row[lnr_pairs[i][0]] # locus
            n = row[lnr_pairs[i][1]] # nr
            kill = [l, n]
            tmp_lk, tmp_he = lookup_new_he(lk, kill)
            tmp_lookups.append(tmp_lk)
            tentative_he += tmp_he
        tentative_he = tentative_he / float(len(lookups))

        raw_input('key to continue')


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
