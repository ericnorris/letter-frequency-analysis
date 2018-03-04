from .analyze import AnalysisResults

from jinja2 import Environment, FileSystemLoader

def htmlgen(counts: AnalysisResults, out_dir: str):
    env = Environment(loader=FileSystemLoader('templates'))

    index_template = env.get_template('index.jinja2')

    with open(out_dir + '/index.html', 'w') as index_file:
        index_template.stream(
            all_symbols_count_desc=counts.all_symbols.most_common(),
            all_symbols_relative_freq=calculate_all_symbols_relative_frequency(counts)
        ).dump(index_file)


def calculate_all_symbols_relative_frequency(counts: AnalysisResults) -> list:
    total = sum(counts.all_symbols.values())

    percentages = sorted([
        (symbol, count / total) for symbol, count in counts.letters.items()
    ])

    percentages.append(('[[:digit:]]', counts.all_symbols['numbers'] / total))
    percentages.append(('[[:punct:]]', counts.all_symbols['punctuation'] / total))
    percentages.append(('[ ]', counts.all_symbols['space'] / total))

    return percentages
