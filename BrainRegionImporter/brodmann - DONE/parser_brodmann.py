#!/usr/bin/env python

# Parameters for Script
# -----
INPUTFILENAME = 'brodmann.csv'
OUTPUTFILENAME = 'outputBRODMANN.txt'
SPECIES = 'Homo sapiens'
WRITEOUTPUT = True

# specials
# -----
#   CAT:Brodmann 1909
#   cytoarchitecture
#   Nr. ->
#   TITLE:BA#
#   NAME:Brodmann area #
#   WL:Brodmann_area_#
#   NL:Category:Brodmann_(1909)_area_#

# Init
# -----
import csv
import pickle
import re

# read in the input csv file
reader = csv.reader(open(INPUTFILENAME, "rb"), delimiter=';')
# containing brain regions
bigdict = {}
# containing wiki reference text for pmid
pmidict = {}

for row in reader:
    print 'processing row:'
    regionname = row.pop(0)
    print regionname
    
    tmpdict = {}
    
    for a in row:
        
        alist = a.partition(':')
        
        tmpdict[alist[0]] = alist[2]
    
    bigdict[regionname] = tmpdict
    print '------'
    

regionpage = """\
{{Connectome Brain Region
|Abbreviation=#F1#
|Species=%s
|English Name=#F2#
|Latin Name=#F3#
|Other Name=#F8#
|Defining Criteria=cytoarchitecture
|Definition=#F4#
}}
{{Connectome Brain Region LinkOut
|Wikipedia Link=#F17#
|Neurolex Link=#F16#
}}
= More Information =

== Images ==
<br>

== Neuronal populations ==
<br>

== Putative function ==
<br>

== Electrophysiology data ==
<br>

= References =
#F5#<references/>
[[Category:Brodmann (1909)]]#F6#
{{Connectome Brain Region Hierarchy
|Part of=#F7#
}}
""" % SPECIES

startstring = '{{-start-}}\n'
endstring = '{{-stop-}}\n'

# open outputfile to write
if WRITEOUTPUT:
    text_file = open(OUTPUTFILENAME, "w")

def getfirstauthor(stri):
    for st in stri.split('|'):
        if st.startswith('author='):
            return st

# loop trought bigdict
for region, att in bigdict.items():
    
    # replace fields
    replaced_regionpage = regionpage
    titlestring = "'''BA" + str(region) + "_(" + SPECIES + ")'''\n"
    
    # replace abbreviation
    replaced_regionpage = replaced_regionpage.replace('#F1#', "BA" + str(region))
    
    # replace english name
    replaced_regionpage = replaced_regionpage.replace('#F2#', "Brodmann area " + str(region))
        
    # replace latin name
    if att.has_key('LN'):
        replaced_regionpage = replaced_regionpage.replace('#F3#', att['LN'])

    # replace description / definition
    if att.has_key('DESC'):
        replaced_regionpage = replaced_regionpage.replace('#F4#', att['DESC'])
    
    # replace other name
    if att.has_key('ON'):
        replaced_regionpage = replaced_regionpage.replace('#F8#', att['ON'])
    
    # replace categories
    if att.has_key('CAT'):
        replaced_regionpage = replaced_regionpage.replace('#F6#', att['CAT'])
    
    # replace wikipedia link
    replaced_regionpage = replaced_regionpage.replace('#F17#', "Brodmann_area_" + str(region))

    # replace neurolex
    replaced_regionpage = replaced_regionpage.replace('#F16#', "Category:Brodmann_(1909)_area_" + str(region))

    # replace part of
    if att.has_key('PO'):
        replaced_regionpage = replaced_regionpage.replace('#F7#', att['PO'] + " (" + SPECIES + ")")
        
    # remove the rest of the markers
    p = re.compile('#F\d{1,2}#')
    list2replace = p.findall(replaced_regionpage)
    for match in list2replace:
        replaced_regionpage = replaced_regionpage.replace(str(match), '')
        
    # compose output
    replaced_regionpage = startstring + titlestring + replaced_regionpage + endstring
        
    if WRITEOUTPUT:
        text_file.write(replaced_regionpage + '\n')
    
if WRITEOUTPUT:
    text_file.close()
