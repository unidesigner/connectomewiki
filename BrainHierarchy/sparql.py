for row in g.query('SELECT ?aname ?bname WHERE { ?a foaf:knows ?b . ?a foaf:name ?aname . ?b foaf:name ?bname . }', 
                   initNs=dict(foaf=Namespace("http://xmlns.com/foaf/0.1/"))):
    print "%s knows %s" % row

SELECT ?title
WHERE
{
  <http://example.org/book/book1> <http://purl.org/dc/elements/1.1/title> ?title .
}    

for row in g.query('SELECT ?name WHERE { <http://neurolex.org/wiki/Special:URIResolver/Category-3AStriatum> <http://semantic-mediawiki.org/swivt/1.0#page> ?name . }'):
	print row

from rdflib import Namespace
NLEX = Namespace("http://neurolex.org/wiki/Special:URIResolver/")
ns = dict(nlex=NLEX)
for row in g.query('SELECT ?name WHERE { <http://neurolex.org/wiki/Special:URIResolver/Category-3AStriatum> <http://semantic-mediawiki.org/swivt/1.0#page> ?name . }', initNs=ns):
	print row

for row in g.query('SELECT ?name WHERE { <Category-3AStriatum> <http://semantic-mediawiki.org/swivt/1.0#page> ?name . }', initNs=ns):

SELECT ?name WHERE { <http://neurolex.org/wiki/Special:URIResolver/Category-3AStriatum> <http://semantic-mediawiki.org/swivt/1.0#page> ?name . }


http://neurolex.org/wiki/Special:URIResolver/Category-3AStriatum
http://semantic-mediawiki.org/swivt/1.0#page
http://neurolex.org/wiki/Category:Striatum

