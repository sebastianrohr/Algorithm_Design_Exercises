#!/bin/sh
> out.txt
for FILE in "../data/$*-tsp.txt"
do
    BASE=${FILE%-tsp.txt}
    OUTPUT=$(python3 our_solution.py < $FILE)
    echo "../data/$BASE.tsp: $OUTPUT" >> out.txt
done
diff --strip-trailing-cr out.txt closest-pair-out.txt