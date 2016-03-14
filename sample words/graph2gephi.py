# -*- coding: utf-8 -*-

### reads a 'context' file ("source target" pairs, each in one line) and generates context.gexf file (to be loaded in gephi)
###
### usage:  python ./graph2gephi.py inputfile.txt
###
### generates a inputfile.txt.gexf output file

import sys
import urllib

args = sys.argv
graph = [line.split() for line in open(args[1])]

outFile = args[1] + '.gexf'
f1=open(outFile, 'w+')

f1.write('<graph defaultedgetype="directed">\n\n<nodes>\n')

### print nodes
flat = reduce(lambda x,y: x+y,graph)
words = list(set(flat))
for w in words:
    node =  "<node id='" + w + "' label='" + w + "'/>\n"
    f1.write(urllib.unquote(node))

f1.write("</nodes>\n\n<edges>\n")

### print edges

i = 1
for g in graph:
    node =  "<edge  id='" + str(i) +  "' source='" + g[0] + "' target='" + g[1] + "'/>\n"
    f1.write(urllib.unquote(node))
    i += 1

f1.write("</edges>\n</graph>")

