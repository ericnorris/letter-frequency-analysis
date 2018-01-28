import argparse
import json
import re
import string
import textwrap
from collections import defaultdict
from itertools import chain
from sys import stderr, stdin, stdout


def main():
    pattern = re.compile(
        r"(?P<punct>[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+)" +
        r"|(?P<word>(?:[a-zA-Z])+(?:'[a-zA-Z]+)?)" +
        r"|(?P<number>[0-9]+)"
    )

    letter_counts = defaultdict(int)
    bigram_counts = defaultdict(int)
    trigram_counts = defaultdict(int)
    punctuation_counts = defaultdict(int)
    number_counts = defaultdict(int)

    letter_pos = defaultdict(lambda: {"first": 0, "middle": 0, "last": 0})

    word_count = 0

    for match in chain.from_iterable(pattern.finditer(line) for line in stdin):
        punctuation = match.group("punct") or ""
        word = (match.group("word") or "").lower()
        number = match.group("number") or ""

        if punctuation:
            for character in punctuation:
                punctuation_counts[character] += 1

            continue

        if word:
            word_count += 1
            last_index = len(word) - 1

            for index, letter in enumerate(word):
                if letter == "'":
                    punctuation_counts["'"] += 1
                else:
                    letter_counts[letter] += 1

                if index == 0:
                    letter_pos[letter]['first'] += 1
                elif index == last_index:
                    letter_pos[letter]['last'] += 1
                else:
                    letter_pos[letter]['middle'] += 1

                if index > 0:
                    bigram = word[index - 1:index + 1]

                    bigram_counts[bigram] += 1

                if index > 1:
                    trigram = word[index - 2:index + 1]

                    trigram_counts[trigram] += 1

            continue

        if number:
            for digit in number:
                number_counts[digit] += 1

            continue

    # end for match in...

    json.dump(
        {
            "word-count": word_count,
            "letter-counts": letter_counts,
            "letter-positions": letter_pos,
            "bigram-counts": bigram_counts,
            "trigram-counts": trigram_counts,
            "punctuation-counts": punctuation_counts,
            "number-counts": number_counts,
        },
        stdout,
        sort_keys=True,
        indent=4,
        ensure_ascii=False
    )

    stdout.flush()

    print(
        "Finished, processed {word_count} words.".format(word_count=word_count),
        file=stderr
    )


if __name__ == '__main__':
    argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
            Perform letter frequency analysis on stdin. Expects UTF-8 input, produces UTF-8
            JSON output with the following keys:

              - word-count
              - letter-counts
              - letter-positions
              - bigram-counts
              - trigram-counts
              - punctuation-counts
              - number-counts
    """)).parse_args()

    main()
