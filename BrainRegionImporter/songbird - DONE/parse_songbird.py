#!/usr/bin/env python

# Parameters for Script
# -----
INPUTFILENAME = 'SONGBIRD.csv'
OUTPUTFILENAME = 'outputSONGBIRD.txt'
SPECIES = 'Taeniopygia guttata'
WRITEOUTPUT = True
CREATE_PMID_FILE = False
PMID_FILE_NAME = 'pmid_dict.pkl'
EMAIL_FOR_PMED = 'pmid@connectome.ch'

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

# PMID parser
# -----
# Using BioPython
from Bio import Entrez
from Bio import Medline
Entrez.email = EMAIL_FOR_PMED

def get_wikiref(pmid):
    """ Returns the Wiki cite journal entry for a given Pubmed ID """
    
    handle = Entrez.efetch(db="pubmed", id=pmid, rettype="medline", retmode="text")
    records = Medline.parse(handle)
    records = list(records)
    
    import datetime
    now = datetime.datetime.now()
    jetzt= now.strftime("%Y-%m-%d")
    
    # generate the {{cite journal}} format
        
    for rec in records:
        aut = rec["AU"]
        firstauthor = aut.pop(0)
        coauthors = ", ".join(aut)
        
        # get date of publication
        # CRDT
        datee = rec["CRDT"][0].split('/')[0]
        #if datee == '':
        #    datee = rec["PD"]
        
        outstring = "{{cite journal|title=%s|journal=%s|year=%s|author=%s|coauthors=%s|volume=%s|pages=%s|id=PMID %s|accessdate=%s}}" % \
                    (rec["TI"], rec["JT"], datee, firstauthor, coauthors, rec["VI"], rec["PG"], pmid, jetzt)
        
        # example:
        #{{cite journal|title=|journal=|date=2008/07/31/|first=Cyril|last=Herry|coauthors=i|volume=454|issue=7204|pages=600-606|id=PMID 18615015 {{doi|10.1038/nature07166}}|url=http://www.fmi.ch/downloads/news/2008.07.11.01.luthi.nature.press.release.pdf|format=|accessdate=2009-09-12 }}
        
    return outstring
    


for row in reader:
    print 'processing row:'
    
    regionname = row.pop(0)
    print regionname
    
    tmpdict = {}
    
    for a in row:
        
        alist = a.partition(':')
        
        # manage pmid dict
        if alist[0] == 'PMID':
            idlist = alist[2].split(',')
            tmpdict[alist[0]] = idlist
            
            if CREATE_PMID_FILE:
                for id in idlist:
                    if not pmidict.has_key(id):
                        print "Getting reference for %s " % str(id)
                        pmidict[id] = get_wikiref(pmid = id)
                        print
                        
        else:
            tmpdict[alist[0]] = alist[2]
    
    bigdict[regionname] = tmpdict
    print '------'
    
if CREATE_PMID_FILE:
    output = open(PMID_FILE_NAME, 'wb')
    pickle.dump(pmidict, output)
    output.close()
    print 'PMID dict file generated.'
    exit(1)
else:
    print 'Loading stored PMID dict file...'
    try:
        pkl_file = open(PMID_FILE_NAME, 'rb')
        pmidict = pickle.load(pkl_file)
        pkl_file.close()
        print 'Done.'
    except IOError:
        print 'No PMID dict file existing. Generate one first by setting CREATE_PMID_FILE True!'
    

regionpage = """\
{{Connectome Brain Region
|Abbreviation=#F1#
|Species=%s
|English Name=#F2#
|Latin Name=#F3#
|Defining Criteria=anatomy, connectivity
|Definition=#F4#
}}
{{Connectome Brain Region LinkOut
}}
= More Information =

#F10#
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
[[Category:Foundational Partition]]#F6#
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
    titlestring = "'''" + str(region) + "_(" + SPECIES + ")'''\n"
    
    # replace abbreviation
    replaced_regionpage = replaced_regionpage.replace('#F1#', str(region))
    
    # replace english name
    if att.has_key('NAME'):
        replaced_regionpage = replaced_regionpage.replace('#F2#', att['NAME'])
        
    # replace latin name
    if att.has_key('LN'):
        replaced_regionpage = replaced_regionpage.replace('#F3#', att['LN'])

    # more text
    if att.has_key('TEXT'):
        replaced_regionpage = replaced_regionpage.replace('#F10#', 'Is there a topographical organisation? ' + att['TEXT'])    
       
    
    # replace description / definition
    if att.has_key('DESC'):
        replaced_regionpage = replaced_regionpage.replace('#F4#', att['DESC'])
    
    # replace references
    if att.has_key('PMID'):
        tmpref = []
        for ref in att['PMID']:
            # loop trough the references
            tmpref.append(pmidict[ref])
            
        # sort the references alphanumeric by first author
        tmpref.sort(key = getfirstauthor)
        
        for ref in tmpref:
            replaced_regionpage = replaced_regionpage.replace('#F5#', "* " + ref + '\n#F5#')

    # replace categories
    if att.has_key('CAT'):
        replaced_regionpage = replaced_regionpage.replace('#F6#', att['CAT'])
    
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
