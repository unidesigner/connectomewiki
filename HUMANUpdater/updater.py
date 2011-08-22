# start with: python updater.py
# updates the HUMAN.csv file with Braininfo ids BI: and Bredewiki Interwiki Links BW:
# -> output: HUMAN_output.csv and summary.txt (do manual work)

import csv

braininfofile = csv.DictReader(open('braininfo link.csv'), delimiter=';')
bredewikifile = csv.DictReader(open('bredewiki.csv'))

braininfo = dict()
braininfoacc = dict()
braininfofoundid = [] # lists all the id's that were found in HUMAN.CSV
cwikinotfound = [] # lists all the rows where no braininfo id was found

while True:
    try:
        row = braininfofile.next()
        braininfo[int(row['ID'])] = row['English Long Name']
        braininfoacc[int(row['ID'])] = row['Acronym']
    except StopIteration: break

bredewiki = []
bredewikifound = []
while True:
    try:
        row = bredewikifile.next()
        print 
        bredewiki.append(row['Name'])
    except StopIteration: break

reader = csv.reader(open('HUMAN.csv', "rb"), delimiter=';')
output = csv.writer(open('HUMAN_output.csv', "w"), delimiter=';')

def biname(id):
    """ Returns braininfo name given id """
    return braininfo[id]

def biabbr(id):
    """ Returns braininfo acronym given id """
    return braininfoacc[id]

for row in reader:

    # goal: for every row, find a corresponding
    # BI: id
    # BW: id
    # add them and write to HUMAN_output.csv
    found = False

    # does human abbrev exists in braininfoacc?
    # lowercased, \t pruned
    # if so, print braininfo
    abbrev = row[0].lstrip('\t')
    for k, v in braininfoacc.iteritems():
        if abbrev == v:
            print '----------------------------------------'
            print 'Found the same ACRONYM: ', v, ' has id', k
            print 'Name CW:', row[1]
            print 'Name BI:', biname(k)
            print
            choose = raw_input('[Enter] ok, [1] no ---->')
            if choose == '':
                print 'taken!'
                row.append('BI:' + str(k))
                braininfofoundid.append(k)
                # HACK: make it impossible to find the name afterwards
                braininfo[k] = ''
                found = True
            elif choose == '1':
                print 'not taken, write abbreviation collision to summary file'
                found = False

    # does human name exists in braininfo?
    # if so, print braininfo
    # if several exists, make a mask to choose
    # maybe also compare the abbreviations!?, e.g. add the abbreviations!
    name = row[1].lower()
    for k, v in braininfo.iteritems():
        if name == v: # improve this check, e.g. with regular expression!
            # also take ON:...
            print '----------------------------------------'
            print 'Found the same NAME: ', v, ' has id', k
            print 'Name CW:', row[1]
            print 'Name BI:', v
            print
            choose = raw_input('[Enter] ok, [1] no ---->')
            if choose == '':
                print 'taken!'
                row.append('BI:' + str(k))
                braininfofoundid.append(k)
                # HACK: make it impossible to find afterwards, also no duplicates
                braininfo[k] = ''
                found = True
            elif choose == '1':
                print 'not taken, write name collision to summary file'
                # cw names/lines with no BI, id!
                # found stays False
                found = False
   
    if not found and not row[1].lower() in cwikinotfound:
        # not found in wiki
        cwikinotfound.append(row[1])
        
    # BREDEWIKI
    # use name from above
    print '##################'
    print '#BREDEWIKI       #'
    print '##################'
    name = row[1].lower()
    for bwname in bredewiki:
        if name == bwname.lower():
            print '------------------------------'
            print 'Found Bredewiki entry', bwname
            print 'Info: Add to HUMAN2.csv'
            row.append('BW:' + bwname)
            bredewikifound.append(bwname)
    
    
    # save all the good things!
    output.writerow(row)

# print out the not found bredewiki entries
# filter bredewiki with bredewikifound

def eleminlist(elem, list):
    " Is element in list?"
    for el in list:
        if elem.lower() == el.lower():
            return True
    return False

def elemindict(elem, dict):
    " Is element as as key"

# output
## regions where an id was found ->  already added and stored to HUMAN2.csv
## regions where no id was found -> in text file for manual search

# write summary file!
f = open('summary.txt', 'w')

f.write('\n\n-------------------------------------\n')
f.write('Following Bredewiki entries have not been found in HUMAN2.csv\n')
f.write('FIND THEM MANUALLY!\n')
f.writelines([elem + '\n' for elem in bredewiki if not eleminlist(elem, bredewikifound)])
f.write('\n\n-------------------------------------\n')
f.write('Following items have no Braininfo ID from HUMAN.csv\n')
f.write('YOU MIGHT WANT TO FIND MANUALLY AN BRAININFO ID AND BI:-TAG IT\n')
for item in cwikinotfound:
    f.write(item + '\n')
f.write('\n\n-------------------------------------\n')
f.write('Following Braininfo names have not been found in HUMAN.csv\n')
f.writelines([v + '\n' for k,v in braininfo.iteritems() if not k in braininfofoundid])
f.write('\n\n-------------------------------------\n')
f.write('Should be the same List of Braininfo names which have not been found in HUMAN.csv\n')
for k,v in braininfo.iteritems():
    if not v == '':
        f.write(str(k) + ';' + str(v))
        f.write('\n')
        
f.close()