#!/usr/bin/env python

# what to do with missing references? ignore them.

# Parameters for Script
# -----
INPUTFILENAME = 'RAT_CON.txt'
OUTPUTFILENAME = 'outputRAT_CON.txt'
SPECIES = 'Rattus norvegicus'
WRITEOUTPUT = True
CREATE_PMID_FILE = False
PMID_FILE_NAME = 'pmid_dict_con.pkl'
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

        if not rec.has_key("AU"):
            print rec
            outstring = ''
            continue
        aut = rec["AU"]
        
        firstauthor = aut.pop(0)
        coauthors = ", ".join(aut)
        
        # get date of publication
        # CRDT
        datee = rec["CRDT"][0].split('/')[0]
        #if datee == '':
        #    datee = rec["PD"]
        if rec.has_key("VI"):
            vii = rec["VI"]
        else:
            vii = ''
        outstring = "{{cite journal|title=%s|journal=%s|year=%s|author=%s|coauthors=%s|volume=%s|pages=%s|id=PMID %s|accessdate=%s}}" % \
                    (rec["TI"], rec["JT"], datee, firstauthor, coauthors, vii, rec["PG"], pmid, jetzt)
        
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
            
            if 'n/a' in alist[2]:
                continue
                
            
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
    print 'PMID dict file generateed.'
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
{{Connectome Brain Region Connection
|Abbreviation=#F1#
|Species=%s
|From=#F2#
|To=#F3#
}}
= More Information =

== Images ==
<br>

== Electrophysiology data ==
<br>


= References =
* {{cite journal|title=The anatomy of memory: an interactive overview of the parahippocampal-hippocampal network.|journal=Nature reviews. Neuroscience|year=2009|author=van Strien NM|coauthors=Cappaert NL, Witter MP|volume=10|pages=272-82|id=PMID 19300446|accessdate=2009-11-01}} 
* {{cite book | last = Andersen | first = P. | authorlink = Morris, R., Amaral, D.G., Bliss, T., O'Keefe, J. | coauthors = Lavenex, P. | title = The Hippocampus Book | publisher = Oxford University Press | date = 2007 | location = | pages = 37-114 | url = http://books.google.ch/books?id=zg6oyF1DziQC | doi = | id = | isbn = 978-0195100273 }}
* {{cite book | last = Witter | first = M.P. | authorlink = | coauthors = Wouterlood, F.G. | title = Basic anatomy of the parahippocampal region in monkeys and rats | publisher = Oxford University Press | date = 2002 | location = New York | pages = 35-60 | url = | doi = | id = | isbn = 978-0198509172}}
* {{cite book | last = Paxinos | first = George | authorlink = | coauthors = | title = The Rat Nervous System | publisher = Elsevier Academic Press | date = 2004 | location = San Diego | pages = 637-703 | url = http://books.google.ch/books?id=F5xkDtDL4AUC | doi = | id = | isbn = 978-0125476386 }}
* [http://www.temporal-lobe.com TEMPORAL-LOBE.COM] -  Hippocampal-parahippocampal neuroanatomy of the rat
#F5#<references/>
{{Connection End}}
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
    
    fro = region.split('-')[0]
    too = region.split('-')[1]
    
    replaced_regionpage = replaced_regionpage.replace('#F2#', fro + " (" + SPECIES + ")" )
    replaced_regionpage = replaced_regionpage.replace('#F3#', too + " (" + SPECIES + ")" )
    
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
