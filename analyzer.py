import argparse
import json
import re
import textwrap
from collections import defaultdict
from itertools import chain
from sys import stdin, stdout


def main():
    regex = re.compile("([\W_]*)([^\W_]+(?:'[^\W_]+)?)?", re.UNICODE)

    character_counts = defaultdict(int)
    bigram_counts = defaultdict(int)
    trigram_counts = defaultdict(int)

    letter_pos = defaultdict(lambda: {"first": 0, "middle": 0, "last": 0})

    word_count = 0

    for match in chain.from_iterable(regex.finditer(line) for line in stdin):
        characters = match.group(1)
        word = match.group(2)

        for char in characters:
            character_counts[char] += 1

        if word:
            word_count += 1
            last_index = len(word) - 1
        else:
            continue

        for index, letter in enumerate(word):
            letter = letter.lower()

            character_counts[letter] += 1

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

    # end for match in...

    unwanted_keys = (key for key in ['\t', '\n'] if key in character_counts)

    for unwanted_key in unwanted_keys:
        del character_counts[unwanted_key]

    json.dump(
        {
            "word-count": word_count,
            "character-counts": character_counts,
            "bigram-counts": bigram_counts,
            "trigram-counts": trigram_counts,
            "letter-positions": letter_pos,
        },
        stdout,
        sort_keys=True,
        indent=4,
        ensure_ascii=False
    )

    print("Finished, processed {word_count} words.".format(word_count=word_count))


if __name__ == '__main__':
    argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent("""
            Perform letter frequency analysis on stdin. Expects UTF-8 input, produces UTF-8
            JSON output with the following keys:

              - word-count
              - character-counts
              - bigram-counts
              - trigram-counts
              - letter-pos
    """)).parse_args()

    main()
