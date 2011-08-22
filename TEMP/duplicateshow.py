#!/usr/bin/env python

import csv

reader = csv.reader(open('/media/DATEN/workspace/python_workspace/dup.csv', "rb"))
mylist = []

for row in reader:
    mylist.append(row[0])

mylist2 = []
# the whole content into small lettres
for abbrev in mylist:
    mylist2.append((abbrev.lower()).strip())

# sort list
mylist2.sort()
print mylist2
dupstring = 'Duplicates:'

# find duplicates by pop one and check if still in list

for abbrev in mylist2:
    print abbrev + ';' + str(mylist2.count(abbrev))
    
# do it hardcore slow
#for abbrev in mylist2:
#    abtemp = mylist2.pop()
#    if mylist2.count(abtemp)>0:
#        # means that abtemp is a duplicate
#        dupstring = dupstring + ", " + abtemp
#        # now remove all occurences of abtemp in mylist2
#        while mylist2.count(abtemp) != 0:
#            mylist2.remove(abtemp)
#   #     print abtemp + ": " + str(mylist2.count(abtemp)) + " times"
#print dupstring