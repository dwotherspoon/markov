#!/usr/bin/env python3

import argparse
import pickle
import random

from tokeniser import Tokeniser, ControlTokens

def train(args):
    n = args.n
    with open(args.text, 'rt') as fp:
        tokens = [tok for tok in Tokeniser(fp)]

    data = {}
    prefix = (ControlTokens.NULL,) * n

    for tok in tokens:
        # Clear the prefix if we're starting again.
        if tok == ControlTokens.START:
            prefix = (ControlTokens.NULL,) * n
        # Add current token (suffix) to all tokens in the prefix buffer.
        if not prefix in data:
            data[prefix] = [0, {}]
        data[prefix][0] += 1
        data[prefix][1][tok] = data[prefix][1].get(tok, 0) + 1
        prefix += (tok,)
        prefix = prefix[1:]
    normal_data = normalise_data(data)
    save_data(args.out, normal_data)

def normalise_data(data):
    result = {}
    for k, v in data.items():
        total_weight, suffixes = v
        result[k] = {suff: weight/total_weight for suff, weight in suffixes.items()}
    return result

def save_data(file, data):
    with open(file, "wb") as fp:
        pickle.dump(data, fp)

def load_data(files):
    return pickle.load(open(files, "rb"))
    
def gen(args):
    n = args.n
    data = load_data(args.data)
    result = []
    tok = ControlTokens.START
    prefix = (ControlTokens.NULL,) * n
    while tok not in Tokeniser.TERM_TOKENS:
        result.append(tok)
        tok = make_choice(data, prefix)
        prefix += (tok,)
        prefix = prefix[1:]
    result.append(tok)
    print(result)

# Assumes normalised data
def make_choice(data, prefix):
    assert prefix in data
    suffixes = data[prefix]
    idx = random.random()
    for suffix, weight in suffixes.items():
        if idx <= weight:
            return suffix
        idx -= weight

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-n",
                        type=int,
                        help="Chain size",
                        required=True)

    subparsers = parser.add_subparsers(dest="action",
                                        required=True)
    # Options for training
    parser_train = subparsers.add_parser("TRAIN",
                                            help="Produce TRAINing data set for a text.")
    parser_train.add_argument("--text",
                                help="Input text file",
                                required=True)
    parser_train.add_argument("--out",
                                help="Output data file name",
                                required=True)

    # Options for generating
    parser_gen = subparsers.add_parser("GEN",
                                        help="GENerate text from supplied datasets.")
    parser_gen.add_argument("--data",
                            help="Input data file(s)",
                            required=True)

    # Transfer control to correct function
    args = parser.parse_args()
    if args.action == "TRAIN":
        train(args)
    else:
        gen(args)