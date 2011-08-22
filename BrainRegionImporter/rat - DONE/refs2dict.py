# reads all the lines and extracts the id and pmid
refs = {}

file = open("refs.txt")

while 1:
    line = file.readline()
    if not line:
        break
    # extract id
    a = line.split('</th>')
    id = a[0]
    # extract pmid
    b = a[1].split('/pubmed/')
    c = b[1].split('?dopt')
    pmid = c[0]
    
    # store in dict
    refs[id] = pmid
    
# print dict
print refs