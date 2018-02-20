from .analyze import AnalysisResults

from jinja2 import Environment, FileSystemLoader

def htmlgen(counts: AnalysisResults, out_dir: str):
	env = Environment(loader=FileSystemLoader('templates'))

	index_template = env.get_template('index.jinja2')

	with open(out_dir + '/index.html', 'w') as index_file:
		index_template.stream().dump(index_file)
