import codecs
import sys
import os
import re
import csv
import coords
from os.path import basename

#NOTES (02/26/2015):
# This fix was necessary because the old "make_cxo_csv.py" code was doing the aitoff projection and then that projection
# is done again in the D3 javascript code - leading to slight errors in the placement of objects on the skymap
# This code fixed the cxc_sources.csv file, and removed unneccesary entries. A new version of make_cxo_csv.py now picks up
# where this code left off and applies the same changes to new entries in cxc_sources.csv.

def main(filename):
	records=[]
	i=0
	with open(filename, 'rb') as f:
		reader = csv.reader(f)
		for row in reader:
			RA = row[5]
			DEC = row[6]
			l,b = coords.eq2gal(RA,DEC, b1950=False, dtype='f8')
			#print row[0],row[1],row[2],row[3],row[4],row[5],row[6],l,b,row[11],row[12],row[14],row[15],row[16]
			RAflip = float(RA)*-1
			lflip = float(l)*-1
			#construct output record
			#record = '\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",%f,%f,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"' % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],l,b,row[11],row[12],row[14],row[15],row[16]) 
			record = '\"%s\",\"%s\",\"%s\",%f,%s,%f,%f,\"%s\",\"%s\",%s,\"%s\",\"%s\",\"%s\"' % (row[0],row[1],row[2],RAflip,DEC,lflip,b,row[11],row[12],row[13],row[14],row[15],row[16])
			records.append(record)

   	#print out results
   	#fl = codecs.open('cxc_sources_fix.csv', 'w', 'utf8')
	fl = open('cxc_sources_fix.csv', 'a')
   	line = '\n'.join(records)
   	#fl.write(line + u'\r\n')
   	fl.write(line)
   	fl.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: python %(script)s <filename>' % {"script": inspect.getfile( inspect.currentframe() ) }
	else:
		main( sys.argv[1] )


