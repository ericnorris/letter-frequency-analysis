#!/bin/bash

while output=$(inotifywait ./templates ./lfa); do
    echo "Got event: $output"

    if [[ $output =~ "./lfa" ]]; then
        pip install --upgrade . >/dev/null && echo "Updated module"
    fi

    ./bin/run.py htmlgen --input $1 --outdir $2 && echo "Rendered templates"
done
