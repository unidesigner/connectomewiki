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
    print 'processing row:'
    print row
    print '------'
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
    
    # add dict to tree node attributes
    for k,v in tempdict.iteritems():
        elem.attrib[k] = v
        
    elem.attrib['ename'] = ename
    #print ename
    if ind == oldin:
        
        #parentlist[ind] = elem
        parentdict[ind] = elem
        
        if ind == 0:
            overallroot.append(elem)
            #parentlist.append(elem) # start inserting first element in parentlist
        else:
            #print parentdict
            parentdict[ind-1].append(elem)
            #parentdict[ind-1] = elem
            #parentlist[ind-1].append(elem)
            #parentlist[ind] = elem
            # don't change parentlist since parent should stay the same on this level
    elif ind == oldin + 1:
        # one higher in the hierarchy
        parentdict[ind] = elem
        parentdict[ind-1].append(elem)
        
    else:
        #print elem
        #print ind
        #print parentdict
        #del parentdict[range(ind,len(parentdict))]
        #loop to delete keys
        tempdict = dict()
        for k, v in parentdict.iteritems():
            if k < ind:
                tempdict[k] = v
        parentdict = tempdict
        #del parentlist[ind:len(parentlist)]
    
        if ind == 0:
            overallroot.append(elem)
            parentdict[ind] = elem
        else:
            parentdict[ind] = elem
            parentdict[ind-1].append(elem)
            
    oldin = ind
   
    # is an element in parentdict existing?
    if len(parentdict) > 1:
        # if so, grab the last item and add is as PO to the current elem
        elem.attrib['PO'] = parentdict[len(parentdict)-2].tag
    #print elem.tag

#root.text = "TEXT"
#print(etree.tostring(overallroot, pretty_print=True))
#print(etree.tostring(overallroot, pretty_print=True))

# write formated page to pywikibot-file
regionpage = """\
{{Connectome Brain Region
|Abbreviation=#F1#
|Species=#F3#
|English Name=#F4#
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
#F11#<references/>
[[Category:Foundational Partition]]#F18#

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
    replaced_regionpage = replaced_regionpage.replace('#F4#', att['ename'])
    if att.has_key('LN'):
        replaced_regionpage = replaced_regionpage.replace('#F5#', att['LN'])
    if att.has_key('ON'):
        replaced_regionpage = replaced_regionpage.replace('#F6#', att['ON'])
    if att.has_key('SYN'):
        replaced_regionpage = replaced_regionpage.replace('#F7#', att['SYN'])     
    
    if att.has_key('CRI'):
        replaced_regionpage = replaced_regionpage.replace('#F8#', att['CRI'])
    if att.has_key('DEF'):
        replaced_regionpage = replaced_regionpage.replace('#F9#', att['DEF'])
        
    # links to other wiki
    if att.has_key('FUN'):
        replaced_regionpage = replaced_regionpage.replace('#F10#', att['FUN'])
        
    if att.has_key('REF'):
        replaced_regionpage = replaced_regionpage.replace('#F11#', att['REF'] + '\n#F11#')

    if att.has_key('CAT'):
        if ',' in att['CAT']:
            # process multiple comma separated categories
            splitter = att['CAT'].split(',')
            for x in splitter:
                replaced_regionpage = replaced_regionpage.replace('#F18#', '[[' + 'Category:' + x + ']]#F18#')
        else:
            replaced_regionpage = replaced_regionpage.replace('#F18#', '[[' + 'Category:' + att['CAT'] + ']]')

    if att.has_key('NL'):
        replaced_regionpage = replaced_regionpage.replace('#F16#', att['NL'])
    if att.has_key('WL'):
        replaced_regionpage = replaced_regionpage.replace('#F17#', att['WL'])
    if att.has_key('BI'): # braininfo link
        replaced_regionpage = replaced_regionpage.replace('#F70#', att['BI'])
    if att.has_key('BW'): # bredewiki link
        replaced_regionpage = replaced_regionpage.replace('#F71#', att['BW'])
        
    # multiple POs?!
    if att.has_key('PO'):
        replaced_regionpage = replaced_regionpage.replace('#F12#', att['PO'] + ' (' + species + ') ')
        
    # more attribubtes
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
text_file = open("outputHUMAN.txt", "w")
for element in overallroot.iter():
    #print("%s - %s" % (element.tag, element.text))
    if element.text == None:
        continue
    text_file.write(str(element.text) + '\n')
text_file.close()