#!/usr/bin/env python

import csv
from lxml import etree
import re

species = "Bird"

# read in the input csv file
reader = csv.DictReader(open('BIRD.csv', "rb"), delimiter=';')

#PO: for hierarchy
#IMP: for every!
#CRI: anatomy
#ON: Structure & Karten-Hodos  (or other) Term for Structure, Term:
#ONAb: Karten-Hodos (or other) Abbreviation
#LN: Latin Name Adopted by Forum, 
#LA: Abbreviation for Latin Name Adopted by Forum, 
#NAME: English Name Adopted by Forum: 
#ABBREV: Abbreviation for English Name Adopted by Forum: 
#COM: Comments: 
#REF: References  Pertinent to the New Name: 

overallroot = etree.Element("root")

#tree = etree.ElementTree(overallroot)

for row in reader:
        
    elem = etree.Element(row['ABBREV:'])
    
    for k,v in row.iteritems():
        if k =='ABBREV:':
            continue
        #print k,v
        elem.attrib[k.rstrip(':')] = v
        
    overallroot.append(elem)


#root.text = "TEXT"
#print(etree.tostring(overallroot, pretty_print=True))
print(etree.tostring(overallroot, pretty_print=True))


# write formated page to pywikibot-file
regionpage = """\
{{Connectome Brain Region
|Abbreviation=#F1#
|Species=#F3#
|English Name=#F4#
|Latin Abbreviation=#F2#
|Latin Name=#F5#
|Other Name=#F6#
|Synonym=#F7#
|FreesurferLabelID=#F20#
|Defining Criteria=#F8#
|IsMandatory=#F21#
|Definition=#F18#
|Function Tag=#F10#
|Neural Code=
}}
{{Connectome Brain Region LinkOut
|Wikipedia Link=#F17#
|Neurolex Link=#F16#
|BraininfoID=
|Bredewiki Link=
}}
= More Information =

== Images ==
<br>

== Neuronal populations ==
<br>

== Electrophysiology data ==
<br>

= References =
<references/>
#F11#

{{Connectome Brain Region Hierarchy
|Part of=#F12#
}}
"""

# generate output.txt to invoke
# python pagefromfile.py -file:output.txt -force -notitle

startstring = '{{-start-}}\n'
endstring = '{{-stop-}}\n'

# iterate over whole tree and add wikipedia text to its elements
for element in overallroot.iter():
    att = element.attrib
    #print att
    if len(att) == 0:
        continue
    replaced_regionpage = regionpage
    titlestring = "'''" + str(element.tag) + "_(" + species + ")'''\n"
    replaced_regionpage = replaced_regionpage.replace('#F1#', str(element.tag))
    if att.has_key('LA'):
        replaced_regionpage = replaced_regionpage.replace('#F2#', att['LA'])
    replaced_regionpage = replaced_regionpage.replace('#F3#', species)
    replaced_regionpage = replaced_regionpage.replace('#F4#', att['NAME'])
    if att.has_key('LN'):
        replaced_regionpage = replaced_regionpage.replace('#F5#', att['LN'])
    if att.has_key('ON'):
        if not att['ON'] == '':
            if not len(att['ONAb']):
                replaced_regionpage = replaced_regionpage.replace('#F6#', att['ON'] + ' (' + att['ONAb'] + ')')
            else:
                replaced_regionpage = replaced_regionpage.replace('#F6#', att['ON'])
    if att.has_key('SYN'):
        replaced_regionpage = replaced_regionpage.replace('#F7#', att['SYN'])

    # |FreesurferLabelID=ctx-rh-S_precentral-Inferior-part; 2172
    if att.has_key('FS'):
        replaced_regionpage = replaced_regionpage.replace('#F20#', att['FS'])        
    #  IM:
    replaced_regionpage = replaced_regionpage.replace('#F21#', 'Yes')
    
    replaced_regionpage = replaced_regionpage.replace('#F8#', 'anatomy')
    
    if att.has_key('DEF'):
        replaced_regionpage = replaced_regionpage.replace('#F9#', att['DEF'])
        
    # links to other wiki
    if att.has_key('FUN'):
        replaced_regionpage = replaced_regionpage.replace('#F10#', att['FUN'])
        
    if att.has_key('REF'):
        if not len(att['REF']):
            refs = att['REF'].split(',,')
            for x in refs:
                replaced_regionpage = replaced_regionpage.replace('#F11#', att['REF'] + '\n#F11#')

    if att.has_key('COM'):
        replaced_regionpage = replaced_regionpage.replace('#F18#', att['COM'])

    if att.has_key('NL'):
        replaced_regionpage = replaced_regionpage.replace('#F16#', att['NL'])
    if att.has_key('WL'):
        replaced_regionpage = replaced_regionpage.replace('#F17#', att['WL'])
    if att.has_key('PO'):
        replaced_regionpage = replaced_regionpage.replace('#F12#', att['PO'] + ' (' + species + ') ')
        
    # more attribubtes
    replaced_regionpage = replaced_regionpage.replace('#F11#',
        '* {{cite journal|title=Revised Nomenclature for Avian Telencephalon and Some Related Brainstem Nuclei|journal=THE JOURNAL OF COMPARATIVE NEUROLOGY|date=2004|first=Anton|last=Reiner|coauthors=DJ Perkel, L Bruce, AB Butler, A Csillag, W Kuenzel, L Medina, G Paxinos, T Shimizu, GF Striedter, M Wild, GF Ball, S Durand, O Gunturkun, DW Lee, CV Mello, A Powers, SA White, G Hough, L Kubikova, TV Smulders, K Wada, J Dugas-Ford, S Husband, K Yamamoto, J Yu, C Siang, ED Jarvis|volume=|issue=473|pages=377-414|id= |url=http://avianbrain.org/papers/RevisedNomenclature.pdf|format=|accessdate=2009-06-16 }}' +
        '\n#F11#')
    replaced_regionpage = replaced_regionpage.replace('#F11#',
        '* {{cite web|url=http://avianbrain.org/index.html |title=AvianBrain.org |accessdate=2009-06-16 }}' +
        '\n#F11#')


    if att.has_key('IMP'): #imported from      
        if att['IMP'] == 'Paxinos-HNS':
            replaced_regionpage = replaced_regionpage.replace('#F11#',
                '* {{cite book | last = Paxinos | first = George | title = The Human Nervous System | edition=2nd | publisher = Academic Press | year = 2004 | doi = | url= http://www.sciencedirect.com/science/book/978-0-12-547626-3  | isbn = 978-0-12-547626-3  }}' +
                '\n#F11#')
        elif att['IMP'] == 'NeuroNames':
            replaced_regionpage = replaced_regionpage.replace('#F11#',
                '* BrainInfo (2007), Neuroscience Division, National Primate Research Center, University of Washington, http://www.braininfo.org/' +
                '\n#F11#')
        elif att['IMP'] == 'Wikipedia':
            replaced_regionpage = replaced_regionpage.replace('#F11#',
                '* Wikipedia, the free encyclopedia, http://en.wikipedia.org/' +
                '\n#F11#')
        elif att['IMP'] == 'BrainML':
            replaced_regionpage = replaced_regionpage.replace('#F11#',
                '* BrainML Model Repository, http://brainml.org/' +
                '\n#F11#')
        elif att['IMP'] == 'Neurolex':
            replaced_regionpage = replaced_regionpage.replace('#F11#',
                '* NeuroLex, the Neuroscience Lexicon, http://neurolex.org/wiki/Main_Page' +
                '\n#F11#')

    # replace left out markers by empty string using regular expressions
    p = re.compile('#F\d{1,2}#')
    list2replace = p.findall(replaced_regionpage)
    for match in list2replace:
        replaced_regionpage = replaced_regionpage.replace(str(match), '')
    replaced_regionpage = startstring + titlestring + replaced_regionpage + endstring
    
    # store it in text of element
    element.text = replaced_regionpage

    
# write output
text_file = open("outputBIRD.txt", "w")
for element in overallroot.iter():
    #print("%s - %s" % (element.tag, element.text))
    if element.text == None:
        continue
    text_file.write(str(element.text) + '\n')
text_file.close()