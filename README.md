# ApertiumRDF
datasets &amp; results used when writing "Leveraging RDF Graphs for Crossing Multiple Bilingual Dictionaries" (paper at LREC-2016)

## New-data
This directory contains 'cycle computation' for all English nouns in the Apertium RDF data:

	EN-nouns.txt			15,630 English nouns from Apertium RDF data
	
	EN-dict.txt			15,630 English nouns + their context
	
	Targets-EN.txt			24,356 Potential Targets generated by cycle computation
	
	getData.py			Python script to get gata from Apertium RDF SPARQL server 
					(http://linguistic.linkeddata.es/sparql)
	calculateCycles.py		Python script used for cycle calculation

	
	ApertiumRDF-GraphContexts.ipynb		ipynb notebook document analysing context graphs
	
	ApertiumRDF-PotentialTargtes.ipynb	ipynb notebook document analysing generated Potential Targets


$python get.Data.py en EN-nouns.txt > EN-dict.txt

$python calculateCycles.py EN-dict.txt en v > Targets-EN.txt


