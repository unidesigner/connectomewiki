#!/usr/bin/python
# convert the xml from brainmaps.org to a csv file

import csv
import StringIO
from lxml import etree

f = open('abbrevs.xml', 'r')

tree = etree.parse(f)

#print(etree.tostring(page, pretty_print=True))

root = tree.getroot()

nrele = len(root)
nrcolumn = len(root[0])

abbrevWriter = csv.writer(open('abbrevss.csv', 'w'), delimiter=';')

for i in range(0, nrele):
    newrow = []
    # abbrev
    newrow.append(root[i][0].text)
    # term
    newrow.append(root[i][1].text)
    # species
    newrow.append(root[i][3].text)
    # path
    newrow.append(root[i][2].text)
    abbrevWriter.writerow(newrow)
    
