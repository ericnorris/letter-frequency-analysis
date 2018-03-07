from .analyze import AnalysisResults

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from collections import namedtuple

ChartData = namedtuple('ChartData', ['labels', 'data'])

def htmlgen(counts: AnalysisResults, out_dir: str):
    env = Environment(loader=FileSystemLoader('templates'))
    index_template = env.get_template('index.jinja2')

    with open(out_dir + '/index.html', 'w') as index_file:
        index_template.stream(
            timestamp=datetime.now().isoformat(' '),
            word_count=format_word_count(counts.words),
            characters_chart_data=generate_characters_chart_data(counts),
            characters_relative_freq=calculate_characters_relative_frequency(counts),
            letters_relative_freq=calculate_letters_relative_frequency(counts),
            punctuation_chart_data=generate_punctuation_chart_data(counts),
            digits_chart_data=generate_digits_chart_data(counts),
            top_bigrams=counts.bigrams.most_common(10),
            top_trigrams=counts.trigrams.most_common(10)
        ).dump(index_file)


def format_word_count(word_count: int) -> str:
    return "{:,}".format(word_count)


def generate_characters_chart_data(counts: AnalysisResults) -> ChartData:
    characters = counts.characters.copy()

    characters['&'] = characters.pop('[[:punct:]]', 0)
    characters['#'] = characters.pop('[[:digit:]]', 0)

    return ChartData(*zip(*characters.most_common()))


def calculate_characters_relative_frequency(counts: AnalysisResults) -> list:
    total = sum(counts.characters.values())

    def format_percentage(count: int) -> str:
        return "{:.3f}%".format((count / total) * 100)

    percentages = sorted([
        (character, format_percentage(count))
        for character, count in counts.letters.items()
    ])

    percentages.append(('&nbsp;', format_percentage(counts.characters[' '])))
    percentages.append(('punct', format_percentage(counts.characters['[[:punct:]]'])))
    percentages.append(('digit', format_percentage(counts.characters['[[:digit:]]'])))

    return percentages


def calculate_letters_relative_frequency(counts: AnalysisResults) -> list:
    total = sum(counts.letters.values())

    percentages = sorted([
        (character, ("{:.3f}%".format((count / total) * 100)))
        for character, count in counts.letters.items()
    ])

    return percentages


def generate_punctuation_chart_data(counts: AnalysisResults) -> ChartData:
    return ChartData(*zip(*counts.punctuation.most_common()))


def generate_digits_chart_data(counts: AnalysisResults) -> ChartData:
    return ChartData(*zip(*counts.digits.most_common()))
