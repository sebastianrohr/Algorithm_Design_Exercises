#!/bin/sh
for FILE in data/*.txt;
do
    BASE=${FILE%-tsp.txt};
    echo $FILE;
    python3 red_scare_solution.py < $FILE;
done