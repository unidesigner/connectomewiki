#! /usr/bin/python
# generate pages from the csv
# stephan gerhard, april 2009

import csv
import sys

csvfile = sys.argv[1]

# read the data bassse
#reader = csv.reader(open(csvfile, "rb"))
#for row in reader:
#    print row

# open generated_wikipage.txt for writing

# creates disambig pages (?), create LH, RH

reader = csv.DictReader(open(csvfile), delimiter=";")

# print reader.fieldnames

# initialize the big-nested-dictionary
# goal: dict['ID']['Abbreviation']
allregions = dict()

while True:

	try:
		# read the next row, type dictionary
		row = reader.next()
		# add the row-dict to the allregions-dict with ID as key
		allregions[row['ID']] = row
		
		# Print the parsed data
		#print detail
		#print len(detail)
		#print detail['Abbreviation']

	except StopIteration: break

# subprogram
# parses all the has-properties and replaces it correctly

	#subregions = allregions['ID']['has...']
	# subregions_nr =  map(int, subregions)
	# subregions_list = subregions.split(',')

	# generate all corresponding properties
	#for ele in subregions_list:
		# get the abbreviation to make the property
#		print allregions[ele]['Abbreviation']


# subprogram
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
== References==
#F11#

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

# generate addpages.txt

text_file = open("addpages.txt", "w")

startstring = '{{-start-}}\n'
endstring = '{{-stop-}}\n'

# iterate over all rows of the dict and generate a page for each.

for key, row in allregions.items():
	replaced_regionpage = regionpage
	titlestring = "'''" + row['English Name'] + "_(" + row['Species'] + ")'''\n"
#	replaced_regionpage = replaced_regionpage.replace('#F1#', 'Abbreviation')
#	replaced_regionpage = replaced_regionpage.replace('#F2#', 'Latin Abbreviation')
	replaced_regionpage = replaced_regionpage.replace('#F3#', row['Species'])
	replaced_regionpage = replaced_regionpage.replace('#F4#', row['English Name'])
#	replaced_regionpage = replaced_regionpage.replace('#F5#', 'Latin Name')
#	replaced_regionpage = replaced_regionpage.replace('#F6#', 'Other Name')
#	replaced_regionpage = replaced_regionpage.replace('#F7#', 'Synonym')
#	replaced_regionpage = replaced_regionpage.replace('#F8#', 'Defining Criteria')
#	replaced_regionpage = replaced_regionpage.replace('#F9#', 'Definition')
#	replaced_regionpage = replaced_regionpage.replace('#F10#', 'Function Tag')
#	replaced_regionpage = replaced_regionpage.replace('#F11#', 'References')
#	replaced_regionpage = replaced_regionpage.replace('#F12#', 'Has spatial-functional part')
#	replaced_regionpage = replaced_regionpage.replace('#F13#', 'Has spatial-structural part')
#	replaced_regionpage = replaced_regionpage.replace('#F14#', 'Has afferent')
#	replaced_regionpage = replaced_regionpage.replace('#F15#', 'Has efferent')
#	replaced_regionpage = replaced_regionpage.replace('#F16#', 'Neurolex Link')
#	replaced_regionpage = replaced_regionpage.replace('#F17#', 'Wikipedia Link')
	replaced_regionpage = startstring + titlestring + replaced_regionpage + endstring
	print replaced_regionpage
	text_file.write(replaced_regionpage)

text_file.close()


