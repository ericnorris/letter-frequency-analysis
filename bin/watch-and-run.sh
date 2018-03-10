#!/bin/bash

if ! [[ $1 ]] || ! [[ $2 ]]; then
    echo "usage: $(basename "$0") <analysis-results> <output-directory>"

    exit 1
fi


main() {
    log "Starting"

    ./bin/run.py htmlgen --input $1 --outdir $2 && log "Initial template render"

    while output=$(inotifywait ./templates ./lfa 2>/dev/null); do
        log "Got event: $output"

        ./bin/run.py htmlgen --input $1 --outdir $2 && log "Rendered templates"
    done
}


log() {
    echo "[$(date -u -R)]" "$@"
}


main "$@"
