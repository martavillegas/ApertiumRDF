# -*- coding: utf-8 -*-
import sys
import urllib

args = sys.argv
data = [line.split("'OK', ") for line in open(args[1])]

#tractor ROOT: tractor-n-en ['OK', 'tractor-n-es', (0.65, 3), ['traktoro-n-eo', 'tracteur-n-fr', 'tractor-n-es', 'traktore-n-eu', 'tractor-n-en']]


for d in data:
    items = d[0].split(' ')
    
    d.pop(0)
    for r in d:
        l = r.split(',')
        print(items[0],l[0],l[1], l[2])  #items[0]=root ; l[0]=target ; l[1]=density score ; l[3]=node degree
