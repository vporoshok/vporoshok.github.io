#!/bin/bash

sources=`find . -name '*.mmd'`
for source in $sources; do
    target=${source/.mmd/.svg}
    if [ $source -nt $target ]; then
        mmdc -i $source -o $target
    fi
done
