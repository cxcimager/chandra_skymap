import Image
import codecs
import sys
import os
import re
import csv
import urllib2
import coords
from pyavm import AVM
from os.path import basename

def main(image):

    #initialize variables
    BASE_RESOURCE_URL = 'http://chandra.harvard.edu/photo/'
    web_img = os.path.basename(image)
    filename, fileext = os.path.splitext(image)
    jpg = basename(filename)+".jpg"
    records=[]
    Type = ""
    Dist = ""
    SubType = "None";

    #jpegs seem to work more consistently with pyavm - use the main jpg image for AVM
    try:
        print "Reading AVM from: "+filename+".jpg"
        avm = AVM(filename+'.jpg')
        ThmbLink = BASE_RESOURCE_URL+filename+'_250.jpg'
        ThmbLink2 = BASE_RESOURCE_URL+filename+'_map.jpg'
    except:
        print 'Trouble reading AVM: '+filename+".jpg"
        return 1

    URL = (avm.ReferenceURL).strip('\n')
    Date = avm.Date
    try:
        Name = avm.Subject.Name[0]
    except:
        print "Missing Name:" +filename+".jpg"
    
    try:
        f = urllib2.urlopen(urllib2.Request(ThmbLink2))
        Img = ThmbLink
    except:
        Img = avm.ResourceURL
    if Img == avm.ResourceURL:
        try:
            f = urllib2.urlopen(urllib2.Request(ThmbLink))
            Img = ThmbLink
        except:
            Img = avm.ResourceURL
            print "Missing thumbnail! (" + ThmbLink + "): " + filename+".jpg"
        
    Cat = re.split("\.",avm.Subject.Category[0])
    Title = avm.Title[0].replace('\"','\'')
                    
    try:
        Headline = avm.Headline.replace('\"','\'')
    except:
        print 'Missing Headline:' +filename+".jpg"

                        
    #coordinate conversions
    try:
        Xeq = avm.Spatial.ReferenceValue[0]
        Yeq = avm.Spatial.ReferenceValue[1]
        Xgal,Ygal = coords.eq2gal(Xeq,Yeq, b1950=False, dtype='f8')
        #Xgal,Ygal = coords.radec2aitoff(l,b)
        #Xeq, Yeq = coords.radec2aitoff(RA, DEC)
    except:
        print 'Missing spatial info:' +filename+".jpg"

    #category parser
    if Cat[0] == "A":
        Dist = "SS"
    if Cat[0] == "B":
        Dist = "MW"
    if Cat[0] == "C":
        Dist = "LU"
    if Cat[0] == "D":
        Dist = "EU"
    if Cat[1] == "1":
        Type = "Planet"
    if Cat[1] == "2":
        Type = "IP"
    if Cat[1] == "3":
        Type = "Star"
        try:
            if Cat[2] == "1":
                if Cat[3] == "7":
                    SubType = "WD"
                if Cat[3] == "8":
                    SubType = "SN"
                if Cat[3] == "9":
                    SubType = "NS"
                if Cat[3] == "10":
                    SubType = "BH"
        except:
            return 1
    if Cat[1] == "4":
        Type = "Nebula"
        try:
            if Cat[2] == "1":
                if Cat[3] == "1":
                    SubType = "ISM"
                if Cat[3] == "2":
                    SubType = "SF"
                if Cat[3] == "3":
                    SubType = "PN"
                if Cat[3] == "4":
                    SubType = "SNR"
                if Cat[3] == "5":
                    SubType = "Jet"
        except:
            return 1
    if Cat[1] == "5":
        Type = "Galaxy"
        try:
            if Cat[2] == "1":
                if Cat[3] == "1":
                    SubType = "Spiral"
                if Cat[3] == "2":
                    SubType = "Barred"
                if Cat[3] == "3":
                    SubType = "Lenticular"
                if Cat[3] == "4":
                    SubType = "Elliptical"
                if Cat[3] == "5":
                    SubType = "Ring"
                if Cat[3] == "6":
                    SubType = "Irregular"
                if Cat[3] == "7":
                    SubType = "Interacting"
                if Cat[3] == "8":
                    SubType = "GravLens"
            if Cat[2] == "2":
                if Cat[3] == "1":
                    SubType = "Giant"
                if Cat[3] == "2":
                    SubType = "Dwarf"
            if Cat[2] == "3":
                if Cat[3] == "1":
                    SubType = "Normal"
                if Cat[3] == "2":
                    SubType = "AGN"
                if Cat[3] == "3":
                    SubType = "Starburst"
                if Cat[3] == "4":
                    SubType = "UL"
        except:
            return 1
    if Cat[1] == "6":
        Type = "Cosmology"            
    
    #Coordinate conversions
    #l,b = coords.eq2gal(RA,DEC, b1950=False, dtype='f8')
    #Xgal,Ygal = coords.radec2aitoff(l,b)
    #Xeq, Yeq = coords.radec2aitoff(RA, DEC)
    
    #construct output record
    record = '\"%s\",\"%s\",\"%s\",%f,%f,%f,%f,\"%s\",\"%s\",%s,\"%s\",\"%s\",\"%s\"' % (Dist,Type,SubType,Xeq*-1,Yeq,Xgal[0]*-1,Ygal[0],Title,Name,Date,URL,Headline,Img) 
    records.append(record)
  
    #print out results
    fl = codecs.open('cxc_sources.csv', 'a', 'utf8')
    line = '\n'.join(records)
    fl.write(line + u'\r\n')
    fl.close()

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage: python %(script)s <filename>' % {"script": inspect.getfile( inspect.currentframe() ) }
	else:
		main( sys.argv[1] )


