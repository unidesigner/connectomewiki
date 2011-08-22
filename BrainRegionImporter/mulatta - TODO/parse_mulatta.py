#!/usr/bin/env python

# Parameters for Script
# -----
INPUTFILENAME = 'mulatta2unique.csv'
OUTPUTFILENAME = 'outputMULATTA.txt'
SPECIES = 'Macaca mulatta'
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
    tmpdict = {"NAME": row[1], "ABBR": row[0],}
    if len(row) == 3:
        tmpdict['PO'] = row[2]
    
    bigdict[row[0]] = tmpdict
    print '------'
    
regionpage = """\
{{Connectome Brain Region
|Abbreviation=#F1#
|Species=%s
|English Name=#F3#
|Latin Name=#F5#
|Other Name=#F6#
|Defining Criteria=#F8#
|Definition=#F9#
|Function Tag=#F10#
}}
{{Connectome Brain Region LinkOut
|Wikipedia Link=#F17#
|Neurolex Link=#F16#
|BraininfoID=#F70#
|Bredewiki Link=#F71#
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
* {{cite book | last = Saleem | first = Kadharbatcha S. | authorlink = | coauthors = Nikos K. Logothetis | title = A Combined MRI and Histology Atlas of the Rhesus Monkey Brain | publisher = Academic Press Inc | date = 2006-11-01 | location = | pages = 336 | url = | doi = | id = | isbn = 978-0123725592 }}
#F11#<references/>
[[Category:Foundational Partition]]#F18#

{{Connectome Brain Region Hierarchy
|Part of=#F4#
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
