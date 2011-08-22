#!/usr/bin/env python

import csv
from lxml import etree
import re

species = "Homo sapiens"

# read in the input csv file
reader = csv.reader(open('HUMAN_output_modified.csv', "rb"), delimiter=';')

# current indent to keep track on which hierarchical level we are
oldin = 0
parentlist = []
duplicatelist = []
parentdict = dict()
overallroot = etree.Element("root")

for row in reader:
    #print 'processing row:'
    #print row
    #print '------'
    # number of indents
    ind = row[0].count('\t')
     
    # new Element   
    # abbreviation trimmed
    abbrev = row[0].lstrip('\t')
    elem = etree.Element(abbrev)
    
    # duplicate finding mechanism
    if abbrev.lower() in duplicatelist:
        print "Duplicate found:", abbrev
        exit(0)
    else:
        duplicatelist.append(abbrev.lower())
        
    # english name
    ename = row[1]
    
    # rest is parsed into dict
    tempdict = dict()
    for entry in range(2,len(row)):
       # print row[entry]
        
        # parition the entry
        temptuple = row[entry].partition(':')
        # build up the dictionary
        # TAKE CARE: MULTIPLE KEYS HANDLING
        tempdict[temptuple[0]] = temptuple[2]
        
        # adding the PO attribute from the actual parentdict
        #tempdict['PO'] = 
    if tempdict.has_key('WL'):
        print abbrev + ';' + tempdict['WL']

#root.text = "TEXT"
#print(etree.tostring(overallroot, pretty_print=True))
#print(etree.tostring(overallroot, pretty_print=True))
