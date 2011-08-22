#!/usr/bin/env python

import csv
#from xml.etree.ElementTree import Element, ElementTree, dump # python 2.5
#import xml.etree.ElementTree as ET # python 2.5
from lxml import etree
import re

species = "Homo Sapiens"

# read in the input csv file
reader = csv.reader(open('input.csv', "rb"), delimiter=';')

# current indent to keep track on which hierarchical level we are
oldin = 0
parentlist = []
parentdict = dict()
overallroot = etree.Element("root")

#tree = etree.ElementTree(overallroot)


for row in reader:

    # number of indents
    ind = row[0].count('\t')
     
    # new Element   
    # abbreviation trimmed
    abbrev = row[0].lstrip('\t')
    elem = etree.Element(abbrev)
    
    # english name
    ename = row[1]
    
    # rest is parsed into dict
    tempdict = dict()
    for entry in range(2,len(row)):
        #print row[entry]
        # parition the entry
        temptuple = row[entry].partition(':')
        # build up the dictionary
        # TAKE CARE: MULTIPLE KEYS HANDLING
        tempdict[temptuple[0]] = temptuple[2]
        

    for k,v in tempdict.iteritems():
        elem.attrib[k] = v
    #elem.attrib = tempdict
    elem.attrib['ename'] = ename

    if ind == oldin:
        #parentlist[ind] = elem
        parentdict[ind] = elem
        if ind == 0:
            overallroot.append(elem)
            #parentlist.append(elem) # start inserting first element in parentlist
        else:
            parentdict[ind-1].append(elem)
            #parentlist[ind-1].append(elem)
            #parentlist[ind] = elem
            # don't change parentlist since parent should stay the same on this level
    elif ind == oldin + 1:
        parentdict[ind] = elem
        parentdict[ind-1].append(elem)
        #parentlist.append(elem)
        #parentlist[ind - 1].append(elem)
    else:
        
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
        else:
            parentdict[ind-1].append(elem)
            #parentlist[ind-1].append(elem)
        
    oldin = ind


#root.text = "TEXT"
#print(etree.tostring(overallroot, pretty_print=True))

# write formated page to pywikibot-file
regionpage = """\
{{Connectome Brain Region
|Abbreviation=#F1#
|Latin Abbreviation=#F2#
|Species=#F3#
|English Name=#F4#
|Latin Name=#F5#
|Other Name=#F6#
|Synonym=#F7#
|Defining Criteria=#F8#
|Definition=#F9#
|Function Tag=#F10#
}}
== References ==
#F11#

#F18#

{{Connectome Brain Region Hierarchy
|Has spatial-functional part=#F12#
|Has spatial-structural part=#F13#
}}
{{Connectome Brain Region Connectivity
|Has afferent=#F14#
|Has efferent=#F15#
}}
{{Connectome Brain Region Geometry}}
{{Connectome Brain Region LinkOut
|Neurolex Link=#F16#
|Wikipedia Link=#F17#
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
    if att.has_key('FUN'):
        replaced_regionpage = replaced_regionpage.replace('#F10#', att['FUN'])
    if att.has_key('REF'):
        replaced_regionpage = replaced_regionpage.replace('#F11#', att['REF'] + '\n#F11#')
    elif att['IMP'] == 'Paxinos-HNS':
        replaced_regionpage = replaced_regionpage.replace('#F11#',
            '* {{cite book | last = Paxinos | first = George | title = The Human Nervous System | edition=2nd | publisher = Academic Press | year = 2004 | doi = | url= http://www.sciencedirect.com/science/book/978-0-12-547626-3  | isbn = 978-0-12-547626-3  }}' +
            '\n#F11#')
    if att.has_key('CAT'):
        replaced_regionpage = replaced_regionpage.replace('#F18#', '[[' + att['CAT'] + ']]')
        
#	replaced_regionpage = replaced_regionpage.replace('#F14#', 'Has afferent')
#	replaced_regionpage = replaced_regionpage.replace('#F15#', 'Has efferent')
    if att.has_key('NL'):
        replaced_regionpage = replaced_regionpage.replace('#F16#', att['NL'])
    if att.has_key('WL'):
        replaced_regionpage = replaced_regionpage.replace('#F17#', att['WL'])
        
    # more attribubtes
    if att.has_key('IMP'): #imported from
        replaced_regionpage = replaced_regionpage.replace('#F11#', '[[ImportedFrom::' + att['IMP'] + '| ]]')
    
    hfunpart = ''
    hstrpart = ''
    if len(list(element)) > 0:
        for children in list(element):
            #print children.attrib['HI']
            if  children.attrib['HI'] == 'f': # functional oder structural has part
                hfunpart = hfunpart + children.tag + ' (' + species + '), '
                    
            elif children.attrib['HI'] == 's':
                hstrpart = hstrpart + children.tag + ' (' + species + '), '
                    
        replaced_regionpage = replaced_regionpage.replace('#F12#', hfunpart)
        replaced_regionpage = replaced_regionpage.replace('#F13#', hstrpart)
        
    # replace left out markers by empty string using regular expressions
    p = re.compile('#F\d{1,2}#')
    list2replace = p.findall(replaced_regionpage)
    for match in list2replace:
        replaced_regionpage = replaced_regionpage.replace(str(match), '')
    replaced_regionpage = startstring + titlestring + replaced_regionpage + endstring
    
    # store it in text of element
    element.text = replaced_regionpage

    
# write output
text_file = open("output.txt", "w")
for element in overallroot.iter():
    #print("%s - %s" % (element.tag, element.text))
    if element.text == None:
        continue
    text_file.write(str(element.text) + '\n')
text_file.close()