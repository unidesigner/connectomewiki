#!/usr/bin/env python

import csv
import sys

target = csv.DictReader(open('enrichlatinabbrev.csv'), delimiter=";")
source = csv.DictReader(open('sourceidlatingabbrev.csv'), delimiter=";")

#print target.fieldnames
#print source.fieldnames

# initialize the big-nested-dictionary
# goal: dict['ID']['Abbreviation']
sourcefields = dict()

while True:
	try:
		# read the next row, type dictionary
		row = source.next()
		# add the row-dict to the allregions-dict with ID as key
		sourcefields[row['ID']] = row
		
		# Print the parsed data
		#print detail
		#print len(detail)
		#print detail['Abbreviation']

	except StopIteration: break

targetfields = dict()
while True:

	try:
		# read the next row, type dictionary
		row = target.next()
		# add the row-dict to the allregions-dict with ID as key
		targetfields[row['NN_ID']] = row
		#print row
		# Print the parsed data
		#print detail
		#print len(detail)
		#print detail['Abbreviation']

	except StopIteration: break

# iterate over target fields and check
# if ID is in sourcefield
#  True: enrich target with its entries for abbreviation and latin name
#  False: continue

for nnid in targetfields:
	if sourcefields.has_key(nnid):
		targetfields[nnid]['Abbreviation'] = sourcefields[nnid]['Abbrev']
		targetfields[nnid]['Latin'] = sourcefields[nnid]['Latin']

# write result to csv file
#
#text_file = open("enrichedlist.csv", "w")
#text_file.write('NN_ID;Abbreviation;NN_String;Latin\n')
#
#for key, row in targetfields.items():
#	text_file.write(row['NN_ID']+';'+row['Abbreviation']+';'+row['NN_String']+';'+row['Latin']+'\n')
#
#text_file.close()

# continue merging

almostultimategoal = csv.DictReader(open('surfbirnNN.csv'), delimiter=";")

almostulti = dict()

id = 1
while True:
	try:
		# read the next row, type dictionary
		row = almostultimategoal.next()
		nnid = row['NN_ID']
		almostulti[id] = row
		# check if NN_ID is available in targetfields?
		# if True: add more fields to this row!
		if targetfields.has_key(nnid):
			almostulti[id]['Abbreviation'] = targetfields[nnid]['Abbreviation']
			almostulti[id]['Latin'] = targetfields[nnid]['Latin']
		id = id + 1
		
	except StopIteration: break
	
#endfile = file( "ultimate.csv", "wb" )
#
#fieldnames = almostultimategoal.fieldnames
#fieldnames.append('Abbreviation')
#fieldnames.append('Latin')
#endfile.write(';'.join(fieldnames)+'\n')
#
#ultimatewriter = csv.DictWriter(endfile, fieldnames, delimiter=';', restval='XXXX')
#
##ultimatewriter.writerow(';'.join(fieldnames))
#
#for key, row in almostulti.items():
#	ultimatewriter.writerow(row)
#	
#endfile.close()

# continue merging the last for primates
# load the csv with Abbreviations and neuronames/brainmaps merged
# and enrich them with info BIRN name and Freesurfer Label

primateregions = csv.DictReader(open('allregionsprimate.csv'), delimiter=";")

id = 1
primatesdict = dict()

while True:
	try:
		# read the next row, type dictionary
		row = primateregions.next()
		primatesdict[id] = row

		# check if abbrevation the same as an abbreviation in almostulti(ALLIDS)[Abbreviation]
		# OR lowercased NNBM is a substring of almostulti(ALLIDS)[NN_STRING]
		# True: take the _first_ occurence in almostulti(specificID) and enrich the primatesdict
		# loop over all items in almostulti, this has bad O(n^2)
		for key, row2 in almostulti.items():			
			#if row['Abbrev'].lower() in row2['Abbreviation'] or row['NNBM'].lower() in row2['NN_String'].lower():
			if row['NNBM'].lower() in row2['NN_String'].lower():
				primatesdict[id]['FreeSurfer'] = almostulti[key]['FreeSurfer']
				primatesdict[id]['BIRN_Title'] = almostulti[key]['BIRN_Title']
				primatesdict[id]['Latin'] = almostulti[key]['Latin']
				primatesdict[id]['NN_ID'] = almostulti[key]['NN_ID']
				# print "Found some match!\n"
		id = id + 1
		
	except StopIteration: break

endfile = file( "allprimatesfields2.csv", "wb" )

fieldnames = primateregions.fieldnames
fieldnames.append('FreeSurfer')
fieldnames.append('BIRN_Title')
fieldnames.append('Latin')
fieldnames.append('NN_ID')

endfile.write(';'.join(fieldnames)+'\n')

primateswriter = csv.DictWriter(endfile, fieldnames, delimiter=';', restval='')

#for key, row in primatesdict.items():
#	primateswriter.writerow(row)


endfile.close()

endfile = file( "allprimatesfields2.csv", "wb" )

endfile.write('Abbrev;NNBM\n')

# ALTERNATIVE: JUST CAPITALIZE, abbreviations all uppercase
for key, row in primatesdict.items():
	abbrev = (row['Abbrev'].upper()).strip()
	nnbm = row['NNBM'].capitalize()
	nnbm = nnbm.replace(' (h)','')
	nnbm = nnbm.replace(' (m)','')
	endfile.write(abbrev+';'+nnbm+'\n')

endfile.close()

# THIS WAS KIND A WAST, THE ENRICHMENT IS VERY SPARSE AND ALMOST HELPS NOTHING
# EXCEPT FOR VERY FEW STRUCTURES, ALSO A LOT OF ERRORS IF THIS CRITERION OF STRING
# CONTAINMENT.

# then resolve the duplicates by hand

