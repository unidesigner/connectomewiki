#!/usr/bin/env python

execfile('ren.py')

f = open('protocol2.txt','r')
txt=f.read()
f.close()

# loop over dat and replace all the
# names with their corresponding wiki link style

txt = txt.replace('Anterior:','<br />Anterior:')
txt = txt.replace('Posterior:','<br />Posterior:')
txt = txt.replace('Medial:','<br />Medial:')
txt = txt.replace('Inferior:','<br />Inferior:')
txt = txt.replace('Superior:','<br />Superior:')
txt = txt.replace('Lateral:','<br />Lateral:')

# [[PCS (Homo sapiens)|precentral sulcus]]

for a,b,c in dat:
    if c == '':
        continue
    txt = txt.replace(' ' + b, ' [[%s (Homo sapiens)|%s]]' % (c, b))
    
print txt

f = open('protocol3.txt', 'w')
f.write(txt)
f.close()