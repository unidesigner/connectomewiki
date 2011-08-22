#!/usr/bin/env python

import csv

reader = csv.reader(open('/media/DATEN/workspace/python_workspace/dup2.csv', "rb"))
mylist = []

for row in reader:
    mylist.append(row[0])

# the whole content into small lettres
for abbrev in mylist:
    teststring = (abbrev.lower()).strip()
    if not("sulcus" in abbrev) and not("gyrus" in abbrev):
        print abbrev.capitalize()
