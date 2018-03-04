from .analyze import AnalysisResults

from jinja2 import Environment, FileSystemLoader

def htmlgen(counts: AnalysisResults, out_dir: str):
    env = Environment(loader=FileSystemLoader('templates'))

    index_template = env.get_template('index.jinja2')

    with open(out_dir + '/index.html', 'w') as index_file:
        index_template.stream(
            word_count="{:,}".format(counts.words),
            all_symbols_count_desc=counts.all_symbols.most_common(),
            all_symbols_relative_freq=calculate_all_symbols_relative_frequency(counts),
            letters_relative_freq=calculate_letters_relative_frequency(counts),
            punctuation_count_desc=counts.punctuation.most_common(),
            number_count_desc=counts.numbers.most_common(),
            top_bigrams=counts.bigrams.most_common(10),
            top_trigrams=counts.trigrams.most_common(10)
        ).dump(index_file)


def calculate_all_symbols_relative_frequency(counts: AnalysisResults) -> list:
    total = sum(counts.all_symbols.values())

    percentages = sorted([
        (symbol, count / total) for symbol, count in counts.letters.items()
    ])

    percentages.append(('[[:digit:]]', counts.all_symbols['[[:digit:]]'] / total))
    percentages.append(('[[:punct:]]', counts.all_symbols['[[:punct:]]'] / total))
    percentages.append(('[ ]', counts.all_symbols['[ ]'] / total))

    return percentages

def calculate_letters_relative_frequency(counts: AnalysisResults) -> list:
    total = sum(counts.letters.values())

    percentages = sorted([
        (symbol, count / total) for symbol, count in counts.letters.items()
    ])

    return percentages
