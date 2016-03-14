This ontains the data for EN-ES experiment when running the final algorithm.
This directory contains the data from the final en-es experiment: running the final algorithm against 
the set of English nouns that provided some cycle (we already know these from the previous en-es experiment)


wc -l

   5478 EN-NOUNS.txt		(input en nouns, those that provide some cycle)
   5481 en-es-2.txt		(raw output from cycle computation for the tested en nouns)
   6581 en-es-2-scores.txt	(formated output, "en-es pair + score + degree")
   
scores:

awk 'BEGIN {FS="\t"} {print $3,$4}' en-es-2-scores.txt | sort | uniq -c


    410 0 1
    954 0 2
    133 0 3
     25 0.5 2
     50 0.5 3
     39 0.5333333333333333 3
    220 0.55 2
     20 0.5666666666666667 2
    253 0.5666666666666667 3
     87 0.5666666666666667 4
     27 0.6 1
    107 0.6 3
    173 0.6333333333333333 3
    685 0.6333333333333333 4
    213 0.65 2
    657 0.65 3
     13 0.6666666666666666 3
      8 0.7 2
    680 0.7 4
    214 0.75 2
    926 0.75 3
    687 0.85 3

When degree <3 and score < 0.7 = fail

