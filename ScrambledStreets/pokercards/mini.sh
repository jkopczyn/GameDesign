#!/bin/bash

e=".eps"

for i in 1 3 4 5; do
	for p in "BBW" "BWW" "BWB" "WWB" "WBB" "WBW"; do
		echo $i$p$e
		cp template.eps $i$p$e
	done
done

