#!/usr/bin/env python3

import argparse
import pickle

from tokeniser import Tokeniser

def train(args):
    with open(args.text, 'rt') as fp:
        tokens = [tok for tok in Tokeniser(fp)]
        print(list(tokens[0:1000]))

def gen(args):
    raise NotImplementedError()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action",
                                        required=True)
    # Options for training
    parser_train = subparsers.add_parser("TRAIN",
                                            help="Produce TRAINing data set for a text.")
    parser_train.add_argument("--text",
                                help="Input text file",
                                required=True)

    # Options for generating
    parser_gen = subparsers.add_parser("GEN",
                                        help="GENerate text from supplied datasets.")

    # Transfer control to correct function
    args = parser.parse_args()
    if args.action == "TRAIN":
        train(args)
    else:
        gen(args)