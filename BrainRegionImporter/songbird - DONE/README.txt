Parser Scripts for Python to generate Brain Region / Brain Region Connection
pages from .csv files for the ConnectomeWiki http://www.connectome.ch/wiki/
Including getting wiki-style syntax references from PubMed.

September 2009, Stephan Gerhard (connectome AT unidesign DOT ch)
License: GPLv3, http://gplv3.fsf.org/

Looking at the Python Script, everything should be pretty self-explanatory.
Requirements is BioPython for grabbing the references. Install it from
http://biopython.org/wiki/Main_Page

Generate the output text file by executing in the shell

	python parse_songbird.py

You can modify the scripts as you like, but keep the correct layout as seen in the
string variable 'regionpage'. You can see the current layout if go to a corresponding
wiki page and click on 'edit' (to see the source for a page).

If you have generated an output file and you want to include it in the ConnectomeWiki,
please contact Stephan Gerhard. You will need a Bot login. Then you can use the
PyWikipediaBot from http://pywikipediabot.sourceforge.net/

E.g. by typing in the shell

	python login.py

and then

	 python pagefromfile.py -v -pt:0 -notitle -file:outputSONGBIRD.txt

to include the generated pages.
