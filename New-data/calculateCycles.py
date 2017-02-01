# -*- coding: utf-8 -*-
##################################
##
##
##
## usage: python calculateCycles.py  dict.file  lang  (verbose) >  output.file
##
##################################
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import defaultdict
import sys
import urllib

args = sys.argv
dictionary = args[1]
lang = args[2]

if len(args) == 4:
    verbose = args[3]
else:
    verbose = ""

# Open and read dictionary with format: {noun: [[trans-pairs],[uniq-words]]}
input_file = open(dictionary,'r')
Dict = eval(input_file.read())


def main():
    """Get root word, check if it has a graph and start computation.

    The input dictionary was created bt getData.py and it contains 
    graph/context data from Apertium RDF data for input words.
    """
    for k,v in Dict.items():
        # Get 'root' and corresponding 'translation pairs' and start computation
	if (v[0]):
	    go(k,v[0])
	    

def go(word,graph):
    """Given a root word and its context/graph identify and evaluate potential targets.

    Context/graph contains the list of translation pairs computed 
    by getData.py script).

    Potential targets are those words in the graph that:
    (i) occur in some cycle together with the root word and
    (ii) are not linked to the root.
    
    """
    
    root = str(word) + "-n-" + lang	# Rewrite input word following 'Apertium format'.
    apertium = []			# Used to store already known translations for root.
    pila = []				# Used to control 'already visited nodes'.
    cycles = []                         # Initiate cycles list.
    
    # Read graph and trigger findCycles for each X-Y pair where X=root.
    for pair in graph:                          
        if pair[0] == root: 
       	    findCycles(pair[1],pila,graph,root,cycles)
            apertium.append(pair[1])
    
    # Flat cycles' list to dentify distinct words (using set).
    flat_pairs = reduce(lambda x,y: x+y,graph)   
    uniq_words = list(set(flat_pairs))  

    # Calculate the density of the graph. Density = V / N*(N-1).
    graphD = graphDensity(len(uniq_words),len(graph))   

    if len(cycles) > 0:
        # Remove 'duplicates' in cycles (abc=cba; abcd=abdc) and
        # require len(cycles) > 5 for big contexts (more than 5 known translations).
        cyclesClean = cleanCycles(cycles,root,len(apertium))
        
        if len(cyclesClean) > 0:
            # Identify potential Targets in cycles (nodes not linked to root).
            targets = findTargets(cyclesClean,root,graph)

            # Calculate the cycle density for each potential target
            # For each cycle with a potential target we get: target, density and cycle. 
            cyclesDensity = calculateDensity(cyclesClean,targets,graph)	

            # Get 'already known' target languages.
            languages = getLanguages(apertium)

            # Compute the final score.
            cycles_dict = compute_results(cyclesDensity,graphD,root,languages)
    
            if verbose == 'v':
                # verbose: num of cycles, num of 'uniq' cycles, num words in context, 
                # num translation pairs, num known translations, num potential targets
                info = [len(cycles),len(cyclesClean),len(uniq_words),len(graph),len(apertium),len(targets)]
                info_toprint = ', '.join(map(str, info))

            # Prints: root, target, language, score, graph_density, num_cycles, length_cycles.
            for target, value in cycles_dict.iteritems():
                l = computeLanguages(languages,target)        
                graph_density = '%.3f'%(graphD)
                score = '%.4f'%(value[0])
                if verbose == 'v':
                    print "%s, %s, %s, %s, %s, %s, %s, %s" % (root,info_toprint, graph_density,target,l,score,len(value[1]),len(value[1][0]))
                else:
                    print "%s, %s, %s, %s, %s, %s, %s" % (root,graph_density,target,l,score,len(value[1]),len(value[1][0]))



def compute_results(cyclesDensity,graphD,root,languages):
    """For each potential target compute the final score.

    Input, cyclesDensity: [[target,score,[cycle]], [target,score,[cycle]], ...  
    Each target may occur in several cycles, so we need to choose the best cycles: 
    the [target,score,cycle] tuples with a higher score.
    
    The function builds a dict with {potential_target: [higest_score, [cycles]]}
    """

    cycles_dict = dict()

    # Sort cyclesDensity so that for each target we have the higher score first:
    # [t,08,[cycle]],[t,06,[cycle]],...] 
    for inputCycle in sorted(cyclesDensity, reverse=True):
        target = inputCycle[0]
	score = inputCycle[1]
	cycle = inputCycle[2]
        # If potential target is already in dict, get cycles with same score.
        if target in cycles_dict:
            # If the score in inputCycle equals high_score, get the cycle
            if cycles_dict[target][0] == score:
                cycles_dict[target][1].append(cycle)
        # If target not in dict, add it as { potential_target : [score, [[cycle]] }
        else:
	    l = [score,[cycle]]
	    cycles_dict[target]=l

    #print cycles_dict
    return cycles_dict

    


### Warning:
# We restrict length of cycles to 8 maximum to avoid computation problems:
# bar-n-en:	730 translation pairs (passed)
# hit-n-en:	779 translation pairs (failed)
# leader-n-en:  764 translation pairs (failed)

def findCycles(node,pila,graph,root,cycles):
    """Find cycles in Graph containing root.

    This is a recursive function that starts with node in a 'root-node' pair
    and ends when root is reached (node-root pair).
    """
    pila2add = ""
    # Add node to potential cycle.
    pila.append(node)

    # Look for node/Y pairs in Graph.
    for pair in graph:
        # We had to limit len(cycles) to < 7 to avoid computation problems!  
	if (pair[0] == node and len(pila) < 7):
            # Termination: When pair is "X->root", we reach the end of cycle.    
	    if pair[1] == root:
                # We want cycles bigger than 2 nodes.	   
	        if len(pila) > 1:
	            pila2add = ' '.join(pila)
	            cycles.append(pila2add)
	    else:
                # Check that node is not repeated in cycle.
		if not visited(pair[1],pila):
	            findCycles(pair[1],pila,graph,root,cycles)
    else:
	pila.pop()


# for each cycle, removes inverse cycle (if exists).
#def cleanCycles(cycles,root):
#    cyclesClean = []
#    for cycle in cycles:
#       raw = cycle.split()
#       raw.append(root)
#       raw.reverse()
#       if not raw in cyclesClean:
#            raw.reverse()
#            cyclesClean.append(raw)
#    return(cyclesClean)

# (see above for just removing inverse cycles).

def cleanCycles(cycles,root,apertium):
    """Remove 'redundant' cycles, that is clycles with same nodes 
    and short cycles in big contexts (big contexts are those with more than 5
    already known targets for root). 
    """
    cyclesClean = []
    cyclesSorted = []
    for cycle in cycles:
        raw = cycle.split()
        raw.append(root)
        # If root has more than 5 translations, remove short cyles       
        if (apertium < 6) or (apertium > 5 and len(raw) > 5):          
            check = list(raw)
            check.sort()
            if not check in cyclesSorted:
                cyclesClean.append(raw)
            cyclesSorted.append(check)
    return(cyclesClean)

# Identifies 'potential' Targets in cycles (those not linked to root).

def findTargets(cycles,root,graph):
    global lang
    exists = "no"
    targets = []
    flat = reduce(lambda x,y: x+y,cycles)   # we just flat cycles list to easy
    reduced = list(set(flat))   # we use set to remove duplicates
    reduced.remove(root)        # simply removes root (we don't want root beeing target)
    for word in reduced:
       items = word.split("-")
       if items[-1] != lang:
           for g in graph:
               if ((g[0] == root) & (g[1] == word)):
	           exists = "yes"
           if not exists == "yes":
	       targets.append(word)
           exists = "no"
    return(targets)			


def calculateDensity(cyclesClean,targets,graph):
    """Take cycles containing some Target word and calculate cycle density.
    For each cycle with a potential target we get: target, density and cycle. 
    """
    cyclesDensity = []
    for cycle in cyclesClean:
        l = len(cycle)
        targetsInCycle = []
        # Ceck that cycle contains some target
        for target in targets:
            if target in cycle:
               targetsInCycle.append(target)
        if len(targetsInCycle) > 0:
            score = getDensity(cycle,graph)
            for t in targetsInCycle:
                #cyclesDensity.append([t,l,score,cycle])
		cyclesDensity.append([t,score,cycle])
    return(cyclesDensity)       


def getDensity(cycle,graph):
    """Calculate the density of a cycle, where Density = V / N*(N-1).
    We need to compute the number of vertices between the nodes in the cycle.
    """
    vertice = 0
    for node in cycle:
        for nextNode in cycle:
            # Check if all node pairs in the cycle are linked.
            for g in graph:
                if ((g[0] == node) & (g[1] == nextNode)):
                    vertice += 1
    l = len(cycle)
    result = vertice / float(l * (l-1))
    return(result)

def visited(node, path):
    """Check if a node was already visited.
    """
    return node in path


def graphDensity(nodes,edges):
    """Calculate the density of graph. Density = V / N*(N-1).
    """
    result = edges / float(nodes * (nodes-1))
    return(result)


def getLanguages(apertium):
    """Get languages involved in already known translations
    """
    languages = []
    print("OJO :", apertium)
    for a in apertium:
        items = a.split("-")
        languages.append(items[-1])
    print("OJO :", languages)
    return(languages)


def computeLanguages(languages,target):
    """Check if potential target's lang is already covered by source dict
    """
    items = target.split("-")
    if items[-1] in languages:
       return("1")
    else:
       return("0")


main()
