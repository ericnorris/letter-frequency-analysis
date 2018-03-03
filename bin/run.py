#!/usr/bin/env python3

import lfa

import argparse
import pickle


def main():
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True

    analyze_parser = subparsers.add_parser('analyze')

    analyze_parser.add_argument('--input', required=True, type=argparse.FileType('r'))
    analyze_parser.add_argument('--output', required=True, type=argparse.FileType('wb'))

    htmlgen_parser = subparsers.add_parser('htmlgen')

    htmlgen_parser.add_argument('--input', required=True, type=argparse.FileType('rb'))
    htmlgen_parser.add_argument('--outdir', required=True)

    arguments = parser.parse_args()

    if arguments.command == 'analyze':
        result = lfa.analyze(arguments.input)

        pickle.dump(result, arguments.output)
    elif arguments.command == 'htmlgen':
        counts = pickle.load(arguments.input)

        lfa.htmlgen(counts, arguments.outdir)


if __name__ == '__main__':
    main()
