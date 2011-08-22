#!/usr/bin/env python

# Parameters for Script
# -----
INPUTFILENAME = 'ECONOMO.csv'
OUTPUTFILENAME = 'outputECONOMO.txt'
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

fnames = ['RegionName','EName','LName','Brod','PO']
# read in the input csv file
reader = csv.DictReader(open(INPUTFILENAME, "rb"),delimiter=";", fieldnames=fnames)
# containing brain regions
bigdict = {}
# containing wiki reference text for pmid
pmidict = {}

for row in reader:
    #print row
    if not len(row['Brod'] ) == 0:
        br = row['Brod'].replace(' ', '')
        br = br.split(',')
        row['Brod'] = br
        #print br
    bigdict[row['RegionName']] = row
#    print 'processing row:'
#    regionname = row.pop(0)
#    print regionname
#    
#    tmpdict = {}
#    
#    for a in row:
#        
#        alist = a.partition(':')
#        
#        tmpdict[alist[0]] = alist[2]
#    
#    bigdict[regionname] = tmpdict
#    print '------'
#    
#print bigdict['EK39']

regionpage = """\
{{Connectome Brain Region
|Abbreviation=#F1#
|Species=%s
|English Name=#F2#
|Latin Name=#F3#
|Other Name=#F8#
|Defining Criteria=cytoarchitecture
|Brain Region Partition Scheme=Economo and Koskinas (1925)
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
* {{Cite journal  | last1 = Triarhou | first1 = LC. | last2 = von Economo | first2 = C. | last3 = Koskinas | first3 = GN. | title = A proposed number system for the 107 cortical areas of Economo and Koskinas, and Brodmann area correlations. | journal = Stereotact Funct Neurosurg | volume = 85 | issue = 5 | pages = 204-15 | month =  | year = 2007 | doi = 10.1159/000103259 | PMID = 17534133 }}
#F5#<references/>

{{Connectome Brain Region Hierarchy
|Part of=#F7#
|CorrespondingRegion=#F88#
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
    titlestring = "'''" + str(region) + "_(" + SPECIES + ")'''\n"
    
    # replace abbreviation
    replaced_regionpage = replaced_regionpage.replace('#F1#', str(region))
    
    # replace english name
    replaced_regionpage = replaced_regionpage.replace('#F2#', att['EName'])
        
    # replace latin name
    if att.has_key('LN'):
        replaced_regionpage = replaced_regionpage.replace('#F3#', att['LName'])

    # replace description / definition
    if att.has_key('DESC'):
        replaced_regionpage = replaced_regionpage.replace('#F4#', att['DESC'])
    
    # replace part of
    if att.has_key('PO'):
        replaced_regionpage = replaced_regionpage.replace('#F7#', att['PO'] + " (" + SPECIES + ")")

    # replace part of
    if att.has_key('Brod'):
        for ele in att['Brod']:
            if len(ele) == 0 or ' ' in ele:
                continue
            replaced_regionpage = replaced_regionpage.replace('#F88#', "BA" + ele + " (" + SPECIES + "), #F88#")
        
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
