EN-ES-experiment-1: 
The original en-es translation set was removed and a new one was generated using the cycle algorithm.
Te results are compared against (i) the originl data and (ii) the COSD dictionary (not supplied here 
for copy copyright issues...)

wc -l

  12735 ApertiumNouns-EN-ES.txt		 (original en-es Apertium, reference dict)
  13785 COSD.txt	 		 ('Oxford reference' dictionary, not here)

   5478 EN-NOUNS.txt			 (input en nouns, those that provide some cycle)

					  generated candidates using cycle comptation: 
   6578 toValidate-NoLangRepetition.txt   (en-es candidates + score in NOLangRepetition mode to be validated)
   7007 toValidate-YesLangRepetition.txt  (en-es candidates + score in LangRepetition mode to be validated)

   4902 RESULTS-Oxford-No.txt		  (en-es candidates found in the COSD file -in NOLangRepetition mode)
   5047 RESULTS-Oxford-Yes.txt		  (en-es candidates found in the COSD file -in YESLangRepetition mode)

   5478 No-repetition.txt	 	  (en-es candidates in NOLangRepetition mode, in the 'original format')
   5478 Yes-repetition.txt	 	  (en-es candidates in LangRepetition mode, in the 'original format')
				 

The original format is not very nice and looks like: 

abrasion ROOT: abrasion-n-en []
abscissa ROOT: abscissa-n-en ['OK', 'abscisa-n-es', 0.75, ['abscissa-n-ca', 'abscisa-n-es', 'absciso-n-eo', 'abscissa-n-en']]
...
(abrasion 'provides' no cycle, 'abcissa' gives one cycle with 0.75 density score)


'Validation' against the Apertium original data
===============================================

(1) No Repetition:

fgrep -f ApertiumNouns-EN-ES.txt toValidate-NoLangRepetition.txt > RESULTS-Apertium-No.txt

wc -l RESULTS-Apertium-No.txt = 6578   (all candidates in toValidate...file are also found in the original Apertium file)

awk 'BEGIN {FS="\t"} {print $3}' RESULTS-Apertium-No.txt | sort | uniq -c
      5 0.4666666666666667
    240 0.5
     57 0.5333333333333333
    247 0.55
     29 0.5666666666666667
    108 0.6
    236 0.65
    322 0.6666666666666666
    107 0.7
   2800 0.75
     70 0.8333333333333334
   2357 0.9166666666666666

(2) Yes Repetition:

fgrep -f ApertiumNouns-EN-ES.txt toValidate-YesLangRepetition.txt > RESULTS-Apertium-Yes.txt

 wc -l RESULTS-Apertium-Yes.txt 
7007 RESULTS-Apertium-Yes2.txt     (all candidates in toValidate...file are also found in the original Apertium file)

awk 'BEGIN {FS="\t"} {print $3}' RESULTS-Apertium-Yes.txt | sort | uniq -c
     31 0.4666666666666667
      2 0.47619047619047616
    227 0.5
      3 0.5178571428571429
     90 0.5333333333333333
      4 0.5476190476190477
    232 0.55
    148 0.5666666666666667
      1 0.5714285714285714
    180 0.6
     88 0.6333333333333333
    234 0.65
    371 0.6666666666666666
    130 0.7
   2836 0.75
      3 0.7666666666666667
     70 0.8333333333333334
   2357 0.9166666666666666


(Note: The files RESULTS-Apertium-No.txt and RESULTS-Apertium-Yes.txt are not provided as they can be easily reproduced)


'Validation' against Oxfrord:
=============================

(1) NO repetition:

fgrep -f COSD.txt toValidate-NoLangRepetition.txt > RESULTS-Oxford-No.txt


wc -l RESULTS-Oxford-No.txt 
4902 RESULTS-Oxford-No.txt

awk 'BEGIN {FS="\t"} {print $3}' RESULTS-Oxford-No.txt | sort | uniq -c
      3 0.4666666666666667
     85 0.5
     24 0.5333333333333333
    182 0.55
     20 0.5666666666666667
     42 0.6
    171 0.65
    173 0.6666666666666666
     47 0.7
   2030 0.75
     50 0.8333333333333334
   2075 0.9166666666666666


(2) YES repetition:

fgrep -f COSD.txt toValidate-YesLangRepetition.txt > RESULTS-Oxford-Yes.txt

wc -l RESULTS-Oxford-Yes.txt 
5047 RESULTS-Oxford-Yes.txt

awk 'BEGIN {FS="\t"} {print $3}' RESULTS-Oxford-Yes.txt | sort | uniq -c
     16 0.4666666666666667
     80 0.5
     28 0.5333333333333333
    173 0.55
     61 0.5666666666666667
     69 0.6
     29 0.6333333333333333
    178 0.65
    181 0.6666666666666666
     54 0.7
   2050 0.75
      2 0.7666666666666667
     50 0.8333333333333334
   2075 0.9166666666666666






