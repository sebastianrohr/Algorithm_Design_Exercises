#!/bin/sh
for FILE in *.txt
do
    echo $FILE
	base=${FILE%-in.txt}
    python3 casperMatching.py < $FILE 
done
