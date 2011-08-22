#!/usr/bin/env python

# Parameters for Script
# -----
INPUTFILENAME = 'LAUSANNE.csv'
OUTPUTFILENAME = 'outputLAUSANNE.txt'
SPECIES = 'Homo sapiens'
WRITEOUTPUT = True

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
    print row
    
    tmpdict = {"NAME": row[0], "ABBR": row[1], "PO":row[2], "HEMI": row[3], "CAT": row[4]}
    
    bigdict[row[1]] = tmpdict
    print '------'
    
regionpage = """\
{{Connectome Brain Region Hemisphere
|Abbreviation=#F1#
|Species=%s
|IsHemisphere=#F2#
|English Name=#F3#
}}
#F5#
{{Connectome Brain Region Hierarchy
|Hemispheric part of=#F4#
}}

""" % SPECIES             


startstring = '{{-start-}}\n'
endstring = '{{-stop-}}\n'

# open outputfile to write
if WRITEOUTPUT:
    text_file = open(OUTPUTFILENAME, "w")


# loop trought bigdict
for region, att in bigdict.items():
    
    # replace fields
    replaced_regionpage = regionpage
    titlestring = "'''" + str(region) + "_(" + SPECIES + ")'''\n"
    
    # replace abbreviation
    replaced_regionpage = replaced_regionpage.replace('#F1#', str(region))
    
    # replace english name
    if att.has_key('HEMI'):
        replaced_regionpage = replaced_regionpage.replace('#F2#', att['HEMI'])
        
    # replace latin name
    if att.has_key('NAME'):
        replaced_regionpage = replaced_regionpage.replace('#F3#', att['NAME'])

    # replace categories
    if att.has_key('CAT'):
        replaced_regionpage = replaced_regionpage.replace('#F5#', "[[" + att['CAT'] + "]]")
    
    # replace part of
    if att.has_key('PO'):
        replaced_regionpage = replaced_regionpage.replace('#F4#', att['PO'] + " (" + SPECIES + ")")
        
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
