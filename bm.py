"""
Usage:
    bm-sample.py [options] <input>

Options:
    -h --help  Show this screen.
    -v --verbose  Turn on verbose messages.
    --review  Show overview of D and D'.
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


# is this used for the lookup tables or not?
# when used it seems to return the same few values repeatedly?
def he_lookup_alt(tbl):
    he = tbl.freq.divide(tbl.freq.sum())\
            .apply(lambda x: x / (2 * len(tbl.freq)))\
            .sum()
    return 1 - he


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
    verbose = args['--verbose']
    review = args['--review']

    # setup pairs
    locii_cols = df.filter(like='Locus').columns
    nr_cols = df.filter(regex='[nN][rR]').columns
    lnr_pairs = zip(locii_cols, nr_cols)

    if verbose:
        print 'Locus Columns:', locii_cols
        print 'NR Columns:', nr_cols

    # calculate baseline He
    baseline_he = sum([he_pair(df, a, b) for 
        a, b in lnr_pairs]) / len(lnr_pairs)
    initial_he = baseline_he

    # generate master lookup tables
    lookups = []
    for locus, nr in lnr_pairs:
        lookups.append(lookup_table(df, locus, nr))

    if verbose:
        for i, table in enumerate(lookups):
            print '{}, {} Table:'.format(lnr_pairs[i][0], lnr_pairs[i][1])
            print table.to_string(index=False)

    # being process of random selection
    df_prime = pd.DataFrame(data=None, columns=df.columns, index=df.index)\
            .dropna()
    pool = list(df.index.values)
    tried_but_kept = set()
    bad_eggs = set()
    done = False
    while not done:
        # dataset and tried have same amount, we've tried all possible records
        if len(df) == len(tried_but_kept) or len(df) == 0:
            done = True
            break

        # pick random row
        row_idx = random.sample(pool, 1)
        pool.remove(row_idx)
        row = df.ix[row_idx]

        if verbose:
            print 'Sampled row ({}):'.format(row.Ri.values[0])
            print row.to_string(index=False)

        # calculate temporary He and lookup table for comparison
        tentative_he = 0
        tmp_lookups = []
        for i, lk in enumerate(lookups):
            l = row[lnr_pairs[i][0]] # locus
            n = row[lnr_pairs[i][1]] # nr
            kill = [l, n]
            tmp_lk, tmp_he = lookup_new_he(lk, kill)
            tmp_lookups.append(tmp_lk)
            tentative_he += tmp_he
        tentative_he /= float(len(lookups))

        if tentative_he > baseline_he:
            # record is bad, drop it to D'
            df.drop(row.index, inplace=True)
            df_prime = df_prime.append(row)
            bad_eggs.add(row.index[0])
            lookups = tmp_lookups
            baseline_he = tentative_he
        else:
            # record does not improve He or is equal, keep it
            # TODO: is this correct? will we never come back to this record?
            tried_but_kept.add(row.index[0])

        if verbose:
            print 'Tentative He:', tentative_he
            print 'Improved over {}?: {}'.format(\
                    baseline_he, 'Yes' if tentative_he > baseline_he else 'No')
            print '--'
            print 'Temporary Lookup Tables:'
            for i, table in enumerate(tmp_lookups):
                showoff = table.copy()
                showoff['prob'] = showoff.freq.divide(showoff.freq.sum())
                print lnr_pairs[i][0], lnr_pairs[i][1], 'Table:'
                print showoff.to_string(index=False)
            raw_input('>> Press any key to continue next iteration <<')

    if review or verbose:
        print '\nD Final ({}):'.format(len(df))
        print df.to_string(index=False)
        print '\nD Prime ({}):'.format(len(df_prime))
        print df_prime.to_string(index=False)

    print '\nInitial He:', initial_he
    print 'Final He:', baseline_he


if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
