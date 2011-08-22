#!/usr/bin/env python

# Using BioPython
from Bio import EUtils
from Bio.EUtils import DBIdsClient
from Bio import Medline

PMID="7724575"

client = DBIdsClient.DBIdsClient()
result = client.from_dbids(EUtils.DBIds("pubmed", PMID))
handle=result[0].efetch(rettype="medline", retmode="text")
records = Medline.parse(handle)
records = list(records)

import datetime
now = datetime.datetime.now()
jetzt= now.strftime("%Y-%m-%d")

# generate the {{cite journal}} format

for rec in records:
    aut = rec["AU"]
    firstauthor = aut.pop(0)
    coauthors = ", ".join(aut)
    
    # get date of publication
    # CRDT
    datee = rec["CRDT"].split('/')[0]
    #if datee == '':
    #    datee = rec["PD"]
    
    outstring = "{{cite journal|title=%s|journal=%s|year=%s|author=%s|coauthors=%s|volume=%s|pages=%s|id=PMID %s|accessdate=%s}}" % \
                (rec["TI"], rec["JT"], datee, firstauthor, coauthors, rec["VI"], rec["PG"], PMID, jetzt)
    
    # example:
    #{{cite journal|title=|journal=|date=2008/07/31/|first=Cyril|last=Herry|coauthors=i|volume=454|issue=7204|pages=600-606|id=PMID 18615015 {{doi|10.1038/nature07166}}|url=http://www.fmi.ch/downloads/news/2008.07.11.01.luthi.nature.press.release.pdf|format=|accessdate=2009-09-12 }}
    
print outstring
    