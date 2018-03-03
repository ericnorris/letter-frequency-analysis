import re
from collections import Counter
from itertools import chain
from typing import TextIO

class AnalysisResults:

    def __init__(self):
        self.letters     = Counter()
        self.all_symbols = Counter()
        self.punctuation = Counter()
        self.numbers     = Counter()
        self.bigrams     = Counter()
        self.trigrams    = Counter()

        self.words = 0


def analyze(stream : TextIO) -> AnalysisResults:
    pattern = re.compile(
        r"(?P<punct>[\x21-\x2f\x3a-\x40\x5b-\x60\x7b-\x7e]+)" +
        r"|(?P<word>(?:[a-zA-Z])+(?:'[a-zA-Z]+)?)" +
        r"|(?P<number>[0-9]+)" +
        r"|(?P<space>\b \b)"
    )

    counts = AnalysisResults()

    match_list_iterator = (pattern.finditer(line) for line in stream)
    match_iterator = chain.from_iterable(match_list_iterator)

    for match in match_iterator:
        punctuation = match.group('punct')
        word        = match.group('word')
        number      = match.group('number')
        space       = match.group('space')

        if punctuation:
            counts.punctuation.update(punctuation)

        elif word:
            counts.words += 1

            for index, letter in enumerate(word.lower()):
                if letter == '\'':
                    counts.punctuation[letter] += 1
                else:
                    counts.letters[letter] += 1

                if index > 0:
                    bigram = word[index - 1 : index + 1]

                    counts.bigrams[bigram] += 1

                if index > 1:
                    trigram = word[index - 2 : index + 1]

                    counts.trigrams[trigram] += 1

        elif number:
            counts.numbers.update(number)

        elif space:
            counts.all_symbols['space'] += 1

    # end for match in...

    counts.all_symbols.update(counts.letters)
    counts.all_symbols['punctuation'] = sum(counts.punctuation.values())
    counts.all_symbols['numbers'] = sum(counts.numbers.values())

    return counts
