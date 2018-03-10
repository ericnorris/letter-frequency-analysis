SHELL := /bin/bash

.PHONY: all corpus-from-scratch
.INTERMEDIATE: corpus/OANC-1.0.1-UTF8.zip

all: docs/index.html

corpus-from-scratch: corpus/OANC-1.0.1-UTF8.zip corpus/OANC-1.0.1-UTF8-textonly.gz


docs/index.html: results/oanc-counts.pickle venv/lfa-installed
	source venv/bin/activate && \
		bin/run.py htmlgen --input $< --outdir docs/


results/oanc-counts.pickle: corpus/OANC-1.0.1-UTF8-textonly.gz venv/lfa-installed
	source venv/bin/activate && \
		gzip -d --stdout $< | bin/run.py analyze --input - --output $@


venv/lfa-installed: venv/bin/activate
	source venv/bin/activate && \
		{ pip freeze | grep -q "Letter-Frequency-Analysis"; } || pip install -e .

	touch venv/lfa-installed

venv/bin/activate: requirements.txt
	[[ -d venv/ ]] || virtualenv venv

	source venv/bin/activate && \
		pip install -r requirements.txt

	touch venv/bin/activate


corpus/OANC-1.0.1-UTF8-textonly.gz: corpus/OANC-1.0.1-UTF8.zip
	unzip -p $< "OANC/data/*.txt" | gzip --best > $@

corpus/OANC-1.0.1-UTF8.zip:
	cd corpus && curl -O http://www.anc.org/OANC/OANC-1.0.1-UTF8.zip
