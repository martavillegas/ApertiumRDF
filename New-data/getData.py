# -*- coding: utf-8 -*-

######################################################################################
###
### Reads inputfile (with one noun per line) and calculates their 'context'
### Output is written in a 'dict' file to be used in cycle computation.
###
### usage: python getData.py input.file language dict.file
###
###
### context: list of translation pairs obtained when looking for trans(trans(trans(root)))
### language: en, es ...
### sparql endpoint: http://linguistic.linkeddata.es/sparql
### dictionary format: {noun: [[trans-pairs],[uniq-words]]}
###
#######################################################################################

from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import sys
import urllib

sparql = SPARQLWrapper("http://linguistic.linkeddata.es/sparql")
args = sys.argv

# reads input file and removes duplicates if any
source = [line.rstrip('\n') for line in open(args[1])]

# print source

lang = args[2]


#data = {}

def main(source):
    #global data
    for root in source:
        getGraph(root)
	#print root

    #f = open(dictionary,'w')
    #f.write(str(data))

    	

def getGraph(root):
    #global data
    data = {}
    pairs_words = []
    all_targets = []
    pairs = []
    # get root translations (results)................................... root trans
    results = getSparql(root,lang)
    # for each root trans
    for result in results["results"]["bindings"]:
	# appends root-trans pair
        pairs.append([result["source"]["value"],result["target"]["value"]])  
	#get trans translations (targets) 
        targets = getSparql2(result["target"]["value"]) #............. trans trans2            
        for target in targets["results"]["bindings"]:                         
            pairs.append([result["target"]["value"],target["target"]["value"]])
            #to avoid target duplicates and asking again for root
            if (target["target"]["value"] not in all_targets) & (target["target"]["value"] != result["source"]["value"]): 
                all_targets.append(target["target"]["value"])
                far_targets = getSparql2(target["target"]["value"])#... trans2 trans3
                for far_target in far_targets["results"]["bindings"]:
                    pairs.append([target["target"]["value"],far_target["target"]["value"]])
    if pairs:
        # convert long URIS into 'words'
        for p in pairs:  
            heads = str(p[0]).split('/')			 # str() to convert unicode to utf (avoid the u' thing)
            tails = str(p[1]).split('/')
            pairs_words.append([urllib.unquote(heads[-1]) ,urllib.unquote(tails[-1]) ])
            #print(heads[-1],tails[-1])

        pairs_set = set(map(tuple,pairs_words))  		# using sets to remove duplicates
        pairs_uniq = map(list,pairs_set)			# back to list once duplicates removed
        flat_pairs = reduce(lambda x,y: x+y,pairs_uniq)	# we just flat cycles list to easy dentify distinct words
        uniq = list(set(flat_pairs))			# get distinct words

        data[root] = [ pairs_uniq, uniq ]
        #print('Root', root)
        #print('Words in context', uniq)
        #print('Num words in context',len(uniq))    
        #print('Num of translation pairs',len(pairs_uniq))  
        #print('Pairs',  pairs_uniq) 

        #print(data)
    else:
        data[root] = [ [], [] ]
    
    print str(data)

# gets translations from sparql server (for translation words)

def getSparql2(source):
    head = """
PREFIX lemon: <http://www.lemon-model.net/lemon#>
PREFIX tr: <http://purl.org/net/translation#>
PREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>
SELECT DISTINCT ?source ?target 
WHERE {
  ?sense_source lemon:isSenseOf <"""

    tail = """
  ?trans  tr:translationSense  ?sense_source .
  ?trans  tr:translationSense  ?sense_target .
  ?sense_source lemon:isSenseOf  ?source . 
  ?sense_target lemon:isSenseOf  ?target . 
  FILTER (?source != ?target)}"""

    query = head + source + ">." + tail
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
   # print(results) 
    return(results)

# gets translations from sparql server (for root word)

def getSparql(word,lang):

    head = """
PREFIX lemon: <http://www.lemon-model.net/lemon#>
PREFIX tr: <http://purl.org/net/translation#>
PREFIX lexinfo: <http://www.lexinfo.net/ontology/2.0/lexinfo#>
SELECT DISTINCT ?source ?target 
WHERE {
  ?form_source lemon:writtenRep '"""

    tail = """
  ?source lemon:lexicalForm ?form_source .
  ?source lexinfo:partOfSpeech lexinfo:noun .
  ?sense_source lemon:isSenseOf  ?source .
  ?trans  tr:translationSense  ?sense_source .
  ?trans  tr:translationSense  ?sense_target .
  ?sense_target lemon:isSenseOf  ?target . 
  ?lexicon lemon:entry ?target .
  FILTER (?source != ?target)}"""

    query = head + word + "'@" + lang + "." + tail 
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return(results)

main(source)



