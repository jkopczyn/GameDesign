#! /bin/bash

for d in */ ; do
    echo $d
    cd $d
    for f in *; do
        mv ../$f .
    done
    cd ..
done
